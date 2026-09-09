import logging
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.config.config import GEMINI_MODEL_NAME
from src.config.database import async_session_factory
from src.schema.chat import ChatSession, ChatMessage

logger = logging.getLogger(__name__)


# 1. Define strict structured output schema
class SessionSummaryOutput(BaseModel):
    title: Optional[str] = Field(
        default=None,
        description="A concise 3-6 word title for this conversation session.",
    )
    summary: str = Field(
        description="A dense, factual 2-4 sentence summary capturing goals, key decisions, metrics discussed, and status."
    )


async def update_session_summary_background(session_id: str):
    """
    Background worker that fetches recent messages and produces
    a title and updated summary for the chat session.
    """
    async with async_session_factory() as db:
        try:
            # 1. Fetch current session record
            stmt = select(ChatSession).where(ChatSession.id == session_id).limit(1)
            result = await db.execute(stmt)
            session = result.scalar_one_or_none()
            if not session:
                logger.warning(f"[SummaryWorker] Session {session_id} not found.")
                return

            # 2. Fetch last 10 messages
            msg_stmt = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at.desc())
                .limit(10)
            )
            msg_res = await db.execute(msg_stmt)
            recent_msgs = list(reversed(msg_res.scalars().all()))

            if not recent_msgs:
                logger.warning(
                    f"[SummaryWorker] No messages found for session {session_id}."
                )
                return

            transcript = "\n".join(
                f"{m.role.upper()}: {m.content}" for m in recent_msgs
            )

            prompt = (
                f"CURRENT TITLE: {session.title or 'None'}\n"
                f"CURRENT SUMMARY: {session.summary or 'None'}\n\n"
                f"RECENT MESSAGES:\n{transcript}\n\n"
                "Provide an updated session title and a 2-4 sentence dense factual summary."
            )

            # 3. Use structured output instead of raw text parsing
            llm = ChatGoogleGenerativeAI(
                model=GEMINI_MODEL_NAME,
                temperature=0.0,
            ).with_structured_output(SessionSummaryOutput)

            result: SessionSummaryOutput = await llm.ainvoke(
                [
                    SystemMessage(
                        content="You are an assistant that summarizes user-agent business consultations."
                    ),
                    HumanMessage(content=prompt),
                ]
            )

            new_title = result.title or session.title
            new_summary = result.summary or session.summary

            # 4. Persist update
            upd_stmt = (
                update(ChatSession)
                .where(ChatSession.id == session_id)
                .values(
                    title=new_title,
                    summary=new_summary,
                    updated_at=datetime.now(timezone.utc),
                )
            )
            await db.execute(upd_stmt)
            await db.commit()
            logger.info(
                f"[SummaryWorker] Successfully updated summary for session {session_id}"
            )

        except Exception as e:
            await db.rollback()
            logger.exception(
                f"[SummaryWorker] Error updating summary for session {session_id}: {e}"
            )
