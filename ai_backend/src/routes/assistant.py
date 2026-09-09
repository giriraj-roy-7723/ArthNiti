import asyncio
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.agents.business_agent import get_business_agent
from src.config.database import get_db
import src.config.langgraph as langgraph_config
from src.middlewares.role import require_enterpreneur
from src.schema.enterpreneur import Enterpreneur
from src.schema.chat import ChatSession, ChatMessage, ChatMessageTranslation
from src.utils.translator_utils import Translator
from src.services.chat_summary_service import update_session_summary_background

router = APIRouter()


class ChatRequest(BaseModel):
    business_id: str
    message: str
    session_id: Optional[str] = None
    language: str = "en"


class ChatResponse(BaseModel):
    response: str
    session_id: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    try:
        translator = Translator()
        is_foreign_lang = request.language.lower() not in ["en", "english"]

        # 1. Translate incoming user message to English if necessary (Non-blocking)
        english_user_message = request.message
        if is_foreign_lang:
            english_user_message = await asyncio.to_thread(
                translator.translate,
                text=request.message,
                source_language=request.language,
                target_language="en",
            )

        # 2. Resolve or Create Chat Session
        if request.session_id:
            stmt = select(ChatSession).where(ChatSession.id == request.session_id)
            result = await db.execute(stmt)
            session = result.scalar_one_or_none()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            session_id = session.id
        else:
            new_session = ChatSession(
                user_id=entrepreneur.user_id, business_id=request.business_id
            )
            db.add(new_session)
            await db.flush()
            session_id = new_session.id

        # 3. Persist the ENGLISH user message and its original translation
        user_message_record = ChatMessage(
            session_id=session_id, role="user", content=english_user_message
        )
        db.add(user_message_record)
        await db.flush()

        if is_foreign_lang:
            user_translation = ChatMessageTranslation(
                message_id=user_message_record.id,
                language=request.language,
                content=request.message,
            )
            db.add(user_translation)

        await db.commit()

        # 4. Initialize Agent
        workflow, user_details, entrepreneur_details = await get_business_agent(
            db=db,
            business_id=request.business_id,
            user_id=entrepreneur.user_id,
        )

        if langgraph_config.checkpointer is None:
            raise RuntimeError("LangGraph checkpointer is not initialized")

        agent = workflow.compile(checkpointer=langgraph_config.checkpointer)
        config = {"configurable": {"thread_id": session_id}}

        # 5. Execute Agent using the pure English message
        result = await agent.ainvoke(
            {
                "messages": [("user", english_user_message)],
                "user_details": user_details,
                "entrepreneur_details": entrepreneur_details,
            },
            config=config,
        )

        raw_content = result["messages"][-1].content

        if isinstance(raw_content, list):
            english_agent_response = "".join(
                block.get("text", "")
                for block in raw_content
                if isinstance(block, dict)
            )
        else:
            english_agent_response = str(raw_content)

        # 6. Persist the generated agent response in English
        agent_message_record = ChatMessage(
            session_id=session_id, role="agent", content=english_agent_response
        )
        db.add(agent_message_record)
        await db.flush()

        # 7. Translate the response back (Non-blocking) and persist
        final_response = english_agent_response
        if is_foreign_lang:
            final_response = await asyncio.to_thread(
                translator.translate,
                text=english_agent_response,
                source_language="en",
                target_language=request.language,
            )

            agent_translation = ChatMessageTranslation(
                message_id=agent_message_record.id,
                language=request.language,
                content=final_response,
            )
            db.add(agent_translation)

        await db.commit()

        # 8. Trigger background summarization without blocking user response
        background_tasks.add_task(update_session_summary_background, session_id)

        return ChatResponse(response=final_response, session_id=session_id)

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
