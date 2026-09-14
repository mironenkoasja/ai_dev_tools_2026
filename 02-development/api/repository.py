"""SQLAlchemy repository boundary.

The rest of the application talks to this module, so changing from SQLite to
another SQLAlchemy-supported database does not require changing views/services.
"""

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from sqlalchemy import delete, select

from .database import ExpenseRecord, ParticipantRecord, SessionLocal, UserRecord


def _user_dict(user):
    return {"username": user.username, "password_hash": user.password_hash, "name": user.name}


def _expense_dict(expense):
    created_at = expense.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    return {
        "id": expense.id,
        "owner": expense.owner,
        "title": expense.title,
        "total": f"{Decimal(expense.total):.2f}",
        "date": expense.date.isoformat(),
        "note": expense.note or "",
        "splitType": expense.split_type,
        "payer": expense.payer,
        "participants": [
            {"name": item.name, "share": f"{Decimal(item.share):.2f}", "isPayer": item.is_payer}
            for item in expense.participants
        ],
        "createdAt": created_at.isoformat().replace("+00:00", "Z"),
    }


def reset_store():
    """Clear all rows; used by tests and local development reset scripts."""
    with SessionLocal.begin() as session:
        session.execute(delete(ParticipantRecord))
        session.execute(delete(ExpenseRecord))
        session.execute(delete(UserRecord))


def save_user(username, password_hash, name):
    with SessionLocal.begin() as session:
        user = UserRecord(username=username, password_hash=password_hash, name=name)
        session.add(user)
        session.flush()
        return deepcopy(_user_dict(user))


def get_user(username):
    if not username:
        return None
    with SessionLocal() as session:
        user = session.get(UserRecord, username)
        return deepcopy(_user_dict(user)) if user else None


def save_expense(expense):
    with SessionLocal.begin() as session:
        user = session.get(UserRecord, expense["owner"])
        if user is None:
            raise ValueError("Expense owner does not exist")
        item = ExpenseRecord(
            id=expense["id"], owner=expense["owner"], title=expense["title"],
            total=Decimal(expense["total"]), date=datetime.fromisoformat(expense["date"]).date(),
            note=expense["note"], split_type=expense["splitType"], payer=expense["payer"],
            created_at=datetime.fromisoformat(expense["createdAt"].replace("Z", "+00:00")),
            participants=[
                ParticipantRecord(name=participant["name"], share=Decimal(participant["share"]),
                                  is_payer=participant["isPayer"], position=position)
                for position, participant in enumerate(expense["participants"])
            ],
        )
        session.add(item)
        session.flush()
        return deepcopy(_expense_dict(item))


def get_expense(expense_id, owner):
    with SessionLocal() as session:
        item = session.scalar(select(ExpenseRecord).where(ExpenseRecord.id == expense_id, ExpenseRecord.owner == owner))
        return deepcopy(_expense_dict(item)) if item else None


def list_expenses(owner, limit=None):
    with SessionLocal() as session:
        statement = select(ExpenseRecord).where(ExpenseRecord.owner == owner).order_by(ExpenseRecord.created_at.desc())
        if limit:
            statement = statement.limit(limit)
        return deepcopy([_expense_dict(item) for item in session.scalars(statement).all()])


def delete_expense(expense_id, owner):
    with SessionLocal.begin() as session:
        item = session.scalar(select(ExpenseRecord).where(ExpenseRecord.id == expense_id, ExpenseRecord.owner == owner))
        if item is None:
            return False
        session.delete(item)
        return True


def seed_demo_user():
    with SessionLocal.begin() as session:
        if session.get(UserRecord, "demo") is None:
            session.add(UserRecord(username="demo", password_hash=make_password("demo"), name="Maya Chen"))


seed_demo_user()
