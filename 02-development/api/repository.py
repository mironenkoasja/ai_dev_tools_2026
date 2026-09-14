"""In-memory repository. Replace this module with Django ORM persistence later."""

from copy import deepcopy

from django.contrib.auth.hashers import make_password

USERS = {}
EXPENSES = {}

# Convenient local-development account. A real user store will replace this.
USERS["demo"] = {"username": "demo", "password_hash": make_password("demo"), "name": "Maya Chen"}


def reset_store():
    USERS.clear()
    EXPENSES.clear()


def save_user(username, password_hash, name):
    USERS[username] = {"username": username, "password_hash": password_hash, "name": name}
    return deepcopy(USERS[username])


def get_user(username):
    user = USERS.get(username)
    return deepcopy(user) if user else None


def save_expense(expense):
    EXPENSES[expense["id"]] = deepcopy(expense)
    return deepcopy(expense)


def get_expense(expense_id, owner):
    expense = EXPENSES.get(expense_id)
    if not expense or expense["owner"] != owner:
        return None
    return deepcopy(expense)


def list_expenses(owner, limit=None):
    expenses = [item for item in EXPENSES.values() if item["owner"] == owner]
    expenses.sort(key=lambda item: item["createdAt"], reverse=True)
    return deepcopy(expenses[:limit] if limit else expenses)


def delete_expense(expense_id, owner):
    expense = get_expense(expense_id, owner)
    if expense is None:
        return False
    del EXPENSES[expense_id]
    return True
