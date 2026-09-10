import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.config.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    business_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(
        String, ForeignKey("chat_sessions.id"), index=True, nullable=False
    )
    role = Column(String, nullable=False)  # 'user' or 'agent'
    content = Column(Text, nullable=False)  # Always stores the English version
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # Optional image attached to this message
    image_url = Column(String, nullable=True)
    image_mime_type = Column(String, nullable=True)

    session = relationship("ChatSession", back_populates="messages")
    # One-to-many relationship mapping a single English message to multiple languages
    translations = relationship(
        "ChatMessageTranslation", back_populates="message", cascade="all, delete-orphan"
    )


class ChatMessageTranslation(Base):
    __tablename__ = "chat_message_translations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = Column(
        String, ForeignKey("chat_messages.id"), index=True, nullable=False
    )
    language = Column(String, index=True, nullable=False)  # e.g., 'bn', 'hi'
    content = Column(Text, nullable=False)  # The translated text
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # Optional image attached to this message
    image_url = Column(String, nullable=True)
    image_mime_type = Column(String, nullable=True)

    message = relationship("ChatMessage", back_populates="translations")

    # Enforce one translation per language for a specific message
    __table_args__ = (
        UniqueConstraint(
            "message_id", "language", name="uq_message_translation_language"
        ),
    )
