from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    tz: Mapped[str] = mapped_column(String(64), default="Asia/Tashkent")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    persona_key: Mapped[str] = mapped_column(String(64))
    language: Mapped[str] = mapped_column(String(16))
    difficulty: Mapped[int] = mapped_column(Integer)
    # active | finished | hung_up | agreed | abandoned
    status: Mapped[str] = mapped_column(String(16), default="active", index=True)
    turns: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    messages: Mapped[list["TrainingMessage"]] = relationship(
        back_populates="session", order_by="TrainingMessage.id", cascade="all, delete-orphan"
    )
    review: Mapped["SessionReview | None"] = relationship(
        back_populates="session", cascade="all, delete-orphan", uselist=False
    )


class TrainingMessage(Base):
    __tablename__ = "training_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("training_sessions.id"), index=True)
    role: Mapped[str] = mapped_column(String(16))  # seller | persona
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    session: Mapped[TrainingSession] = relationship(back_populates="messages")


class SessionReview(Base):
    __tablename__ = "session_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("training_sessions.id"), unique=True, index=True
    )
    score_needs: Mapped[int] = mapped_column(Integer)
    score_value: Mapped[int] = mapped_column(Integer)
    score_objections: Mapped[int] = mapped_column(Integer)
    score_close: Mapped[int] = mapped_column(Integer)
    overall: Mapped[float] = mapped_column(Float)
    ethics_violation: Mapped[bool] = mapped_column(Boolean, default=False)
    ethics_quote: Mapped[str] = mapped_column(Text, default="")
    next_step_with_date: Mapped[bool] = mapped_column(Boolean, default=False)
    question_ratio: Mapped[float] = mapped_column(Float)
    avg_words: Mapped[float] = mapped_column(Float)
    rephrasings: Mapped[list] = mapped_column(JSON)
    strengths: Mapped[list] = mapped_column(JSON)
    summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    session: Mapped[TrainingSession] = relationship(back_populates="review")


class AIUsage(Base):
    __tablename__ = "ai_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose: Mapped[str] = mapped_column(String(32))  # dialog | review | ...
    model: Mapped[str] = mapped_column(String(64))
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cache_write_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cache_read_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, index=True
    )
