from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.agents.business_agent import get_business_agent
from src.config.database import get_db
import src.config.langgraph as langgraph_config
from src.middlewares.role import require_enterpreneur
from src.schema.enterpreneur import Enterpreneur
from src.schema.chat import ChatSession, ChatMessage  # Import new schemas

router = APIRouter()


class ChatRequest(BaseModel):
    business_id: str
    message: str
    session_id: Optional[str] = None  # Added session_id


class ChatResponse(BaseModel):
    response: str
    session_id: str  # Return session_id so frontend can continue the thread


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    try:
        # 1. Resolve or Create Chat Session
        if request.session_id:
            # Verify session exists (Optional but recommended)
            stmt = select(ChatSession).where(ChatSession.id == request.session_id)
            result = await db.execute(stmt)
            session = result.scalar_one_or_none()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            session_id = session.id
        else:
            # Create new session
            new_session = ChatSession(
                user_id=entrepreneur.user_id, business_id=request.business_id
            )
            db.add(new_session)
            await db.flush()  # Generate the ID without committing yet
            session_id = new_session.id

        # 2. Persist the incoming user message
        user_message_record = ChatMessage(
            session_id=session_id, role="user", content=request.message
        )
        db.add(user_message_record)
        await db.commit()

        # 3. Initialize Agent
        workflow, user_details, entrepreneur_details = await get_business_agent(
            db=db,
            business_id=request.business_id,
            user_id=entrepreneur.user_id,
        )

        if langgraph_config.checkpointer is None:
            raise RuntimeError("LangGraph checkpointer is not initialized")

        agent = workflow.compile(checkpointer=langgraph_config.checkpointer)

        # Map LangGraph thread_id to session_id for isolated session memory
        config = {"configurable": {"thread_id": session_id}}

        # 4. Execute Agent
        result = await agent.ainvoke(
            {
                "messages": [("user", request.message)],
                "user_details": user_details,
                "entrepreneur_details": entrepreneur_details,
            },
            config=config,
        )

        raw_content = result["messages"][-1].content

        if isinstance(raw_content, list):
            final_message = "".join(
                block.get("text", "")
                for block in raw_content
                if isinstance(block, dict)
            )
        else:
            final_message = str(raw_content)

        # 5. Persist the generated agent response
        agent_message_record = ChatMessage(
            session_id=session_id, role="agent", content=final_message
        )
        db.add(agent_message_record)
        await db.commit()

        return ChatResponse(response=final_message, session_id=session_id)

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
