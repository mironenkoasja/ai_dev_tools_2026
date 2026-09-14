"""Database setup kept independent from Django's ORM.

Set DATABASE_URL to use another SQLAlchemy-supported database, for example:
  sqlite:///fairshare.sqlite3
  postgresql+psycopg://user:password@localhost/fairshare
"""

import os
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fairshare.sqlite3")
engine_options = {"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, future=True, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class UserRecord(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(150), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    expenses: Mapped[list["ExpenseRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class ExpenseRecord(Base):
    __tablename__ = "expenses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[object] = mapped_column(Date, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False, default="")
    split_type: Mapped[str] = mapped_column(String(10), nullable=False)
    payer: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user: Mapped[UserRecord] = relationship(back_populates="expenses")
    participants: Mapped[list["ParticipantRecord"]] = relationship(
        back_populates="expense", cascade="all, delete-orphan", order_by="ParticipantRecord.position"
    )


class ParticipantRecord(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    expense_id: Mapped[str] = mapped_column(ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    share: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    is_payer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    position: Mapped[int] = mapped_column(nullable=False)
    expense: Mapped[ExpenseRecord] = relationship(back_populates="participants")


def initialize_database():
    Base.metadata.create_all(engine)


initialize_database()
