import json

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from . import repository
from .services import ValidationFailure, create_user, validate_and_build_expense


def _json(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        raise ValidationFailure({"non_field_errors": ["Request body must contain valid JSON."]})


def _errors(errors, status=400):
    return JsonResponse({"detail": "Please correct the highlighted fields.", "errors": errors}, status=status)


def _user(request):
    username = request.session.get("username")
    return repository.get_user(username) if username else None


def _user_response(user):
    return {"username": user["username"], "name": user["name"]}


@ensure_csrf_cookie
@require_http_methods(["GET"])
def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


@csrf_protect
@require_http_methods(["POST"])
def register(request):
    try:
        payload = _json(request)
        user = create_user(payload.get("username"), payload.get("password"), payload.get("name"))
    except ValidationFailure as exc:
        return _errors(exc.errors)
    request.session["username"] = user["username"]
    return JsonResponse(_user_response(user), status=201)


@csrf_protect
@require_http_methods(["POST"])
def login(request):
    try:
        payload = _json(request)
    except ValidationFailure as exc:
        return _errors(exc.errors)
    user = repository.get_user(str(payload.get("username", "")).strip())
    if not user or not check_password(str(payload.get("password", "")), user["password_hash"]):
        return JsonResponse({"detail": "Invalid username or password."}, status=401)
    request.session["username"] = user["username"]
    return JsonResponse(_user_response(user))


@require_http_methods(["GET"])
def me(request):
    user = _user(request)
    if not user:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)
    return JsonResponse(_user_response(user))


@csrf_protect
@require_http_methods(["POST"])
def logout(request):
    if not _user(request):
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)
    request.session.flush()
    return HttpResponse(status=204)


@csrf_protect
@require_http_methods(["GET", "POST"])
def expenses(request):
    user = _user(request)
    if not user:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)
    if request.method == "GET":
        raw_limit = request.GET.get("limit")
        try:
            limit = int(raw_limit) if raw_limit else None
            if limit is not None and not 1 <= limit <= 100:
                raise ValueError
        except ValueError:
            return _errors({"limit": ["Limit must be between 1 and 100."]})
        return JsonResponse(repository.list_expenses(user["username"], limit), safe=False)
    try:
        expense = validate_and_build_expense(_json(request), user["username"])
    except ValidationFailure as exc:
        return _errors(exc.errors)
    return JsonResponse(repository.save_expense(expense), status=201)


@csrf_protect
@require_http_methods(["GET", "DELETE"])
def expense_detail(request, expense_id):
    user = _user(request)
    if not user:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)
    expense = repository.get_expense(expense_id, user["username"])
    if expense is None:
        return JsonResponse({"detail": "Expense not found."}, status=404)
    if request.method == "DELETE":
        repository.delete_expense(expense_id, user["username"])
        return HttpResponse(status=204)
    return JsonResponse(expense)
