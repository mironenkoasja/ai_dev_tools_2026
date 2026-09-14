from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from uuid import uuid4

from django.contrib.auth.hashers import make_password

from . import repository

CENT = Decimal("0.01")


class ValidationFailure(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validation failed")


def _error(field, message):
    return {field: [message]}


def _money(value, field, positive=False):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValidationFailure(_error(field, "Enter a valid amount."))
    if not amount.is_finite() or amount < 0 or (positive and amount <= 0):
        raise ValidationFailure(_error(field, "Amount must be greater than zero." if positive else "Amount cannot be negative."))
    if amount.as_tuple().exponent < -2:
        raise ValidationFailure(_error(field, "Amount may have at most two decimal places."))
    return amount.quantize(CENT)


def _format_money(value):
    return f"{Decimal(value).quantize(CENT):.2f}"


def validate_and_build_expense(payload, owner):
    if not isinstance(payload, dict):
        raise ValidationFailure({"non_field_errors": ["Request body must be a JSON object."]})

    errors = {}
    title = str(payload.get("title", "")).strip()
    if not title:
        errors["title"] = ["This field is required."]
    elif len(title) > 200:
        errors["title"] = ["Ensure this field has no more than 200 characters."]

    try:
        total = _money(payload.get("total"), "total", positive=True)
    except ValidationFailure as exc:
        errors.update(exc.errors)

    raw_date = payload.get("date")
    try:
        expense_date = date.fromisoformat(raw_date)
    except (TypeError, ValueError):
        errors["date"] = ["Enter a valid date in YYYY-MM-DD format."]

    split_type = payload.get("splitType")
    if split_type not in {"equal", "custom"}:
        errors["splitType"] = ["Choose equal or custom."]

    payer = str(payload.get("payer", "")).strip()
    raw_participants = payload.get("participants")
    if not isinstance(raw_participants, list) or len(raw_participants) < 2:
        errors["participants"] = ["At least two participants are required."]
        raw_participants = []

    names = []
    participant_rows = []
    for index, participant in enumerate(raw_participants):
        if not isinstance(participant, dict):
            errors.setdefault("participants", []).append(f"Participant {index + 1} is invalid.")
            continue
        name = str(participant.get("name", "")).strip()
        if not name:
            errors.setdefault("participants", []).append(f"Participant {index + 1} needs a name.")
        elif len(name) > 100:
            errors.setdefault("participants", []).append(f"Participant {index + 1} name is too long.")
        if name.casefold() in [existing.casefold() for existing in names]:
            errors.setdefault("participants", []).append("Participant names must be unique.")
        names.append(name)
        participant_rows.append((name, participant))

    if payer not in names:
        errors.setdefault("payer", []).append("Payer must be one of the participants.")

    if errors:
        raise ValidationFailure(errors)

    shares = []
    if split_type == "equal":
        total_cents = int(total * 100)
        base, remainder = divmod(total_cents, len(names))
        shares = [Decimal(base + (remainder if index == len(names) - 1 else 0)) / 100 for index in range(len(names))]
    else:
        for _, participant in participant_rows:
            shares.append(_money(participant.get("share"), "participants"))
        if sum(shares, Decimal("0.00")) != total:
            raise ValidationFailure({"non_field_errors": [f"Custom shares must add up to €{_format_money(total)}."]})

    created_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "id": str(uuid4()),
        "owner": owner,
        "title": title,
        "total": _format_money(total),
        "date": expense_date.isoformat(),
        "note": str(payload.get("note") or "").strip(),
        "splitType": split_type,
        "payer": payer,
        "participants": [
            {"name": name, "share": _format_money(share), "isPayer": name == payer}
            for name, share in zip(names, shares)
        ],
        "createdAt": created_at,
    }


def create_user(username, password, name):
    username = str(username or "").strip()
    name = str(name or "").strip()
    errors = {}
    if not username:
        errors["username"] = ["This field is required."]
    elif len(username) > 150:
        errors["username"] = ["Ensure this field has no more than 150 characters."]
    if not password:
        errors["password"] = ["This field is required."]
    if not name:
        errors["name"] = ["This field is required."]
    if username in repository.USERS:
        errors["username"] = ["A user with that username already exists."]
    if errors:
        raise ValidationFailure(errors)
    return repository.save_user(username, make_password(password), name)
