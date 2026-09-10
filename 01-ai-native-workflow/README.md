# Shared Household Chores

A Django homework project for managing chores in one shared household, built
as part of **01 AI Native Workflow**.

The intended application covers assigned chores, recurring tasks, an overdue/today/upcoming
board, takeover of overdue chores, completion history, and categories. See the
[project plan](_docs/plan.md) and [implementation backlog](backlog.md).

## Current progress

The Django scaffold and backlog task 1 (login and shared layout) are complete:

- Django login and CSRF-protected, POST-only logout.
- Login required for household pages, with equal access for all active members.
- Shared Bootstrap layout with navigation and HTMX loaded for future interactions.
- Protected Board, History, and Categories placeholder pages.
- Django Admin for user management, restricted to staff with the appropriate permissions.

Chore models and management, recurrence, board functionality, history, category
management, and Docker Compose are still pending. The placeholder pages do not
yet display or manage chore data.

## Stack

- Python 3.13 and Django 5.2.17.
- SQLite database (`db.sqlite3`).
- Django Templates, Bootstrap 5.3.8, and HTMX 2.0.10.

Bootstrap and HTMX load from jsDelivr and require an internet connection.
Navigation and authentication work without JavaScript.

## Run in the existing workspace

Open PowerShell in `01-ai-native-workflow`. The local `.venv` already contains Django.
If your terminal is at the repository root, first run `cd 01-ai-native-workflow`.

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Create an administrator if you have not created one yet:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Start the development server:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ and log in with your account. Stop the server with
`Ctrl+C`. These commands use the virtual environment directly, so activation is
not required.

## Fresh setup

Install Python 3.13, open PowerShell in this subproject folder, and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

The existing workspace's virtual environment uses a Python runtime under the
repository's `.tools/python` directory. Keep that directory in place when using
this environment. On another machine, recreate `.venv` using the steps above.

## Household accounts

1. Sign in at http://127.0.0.1:8000/admin/ with your superuser account.
2. Under **Users**, add a user and password for each household member.
3. Keep ordinary members active, with **Staff status** and **Superuser status**
   disabled. They need no groups or permissions for household pages.
4. Members sign in at http://127.0.0.1:8000/accounts/login/.

Use Admin to change passwords when needed. There is no public signup or password
reset flow. Creating the first administrator does not create other household members.

## Pages

| URL | Purpose | Access |
| --- | --- | --- |
| `/accounts/login/` | Login form | Public |
| `/` | Board placeholder | Logged-in members |
| `/history/` | Completed-chore history placeholder | Logged-in members |
| `/categories/` | Category management placeholder | Logged-in members |
| `/accounts/logout/` | Logout via the navigation button (POST) | Logged-in members |
| `/admin/` | Django administration | Staff; management actions require permissions |

After login, members return to the requested household page or the board.
After logout, they return to the login page.

## Project layout

```text
config/                 Django settings and project URLs
core/                   Household application, views, and page URLs
  templates/            Shared layout, login form, and household pages
  static/core/          Custom layout and form styling
_docs/plan.md           MVP requirements and scope
backlog.md              Ordered tasks and acceptance criteria
manage.py              Django management commands
requirements.txt       Django dependency
```

`core.apps.CoreConfig` is registered in `config/settings.py`. Django's
`LoginRequiredMiddleware` protects views by default; the built-in login view
remains public.

## Verification

Run Django's system checks from this folder:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

To check the login flow manually, open the board while logged out, log in as an
ordinary member, visit all three navigation pages, and log out. Confirm that the
board requires login again and that ordinary members cannot access Admin.

Task 1 passed system checks and a temporary request-client walkthrough covering
authentication, redirects, CSRF protection, logout, and member/staff access.
Three automated authentication tests cover protected-page redirects, successful
login with a return URL, and logout ending access to household pages. Run them with:

```powershell
.\.venv\Scripts\python.exe manage.py test core
```

Django creates an isolated test database; these tests do not change your local
household users or data. Other scenarios, including CSRF enforcement and visual
layout checks, are not covered by these three tests.

The settings are for local development. Docker Compose setup is planned in
backlog task 7; `docker compose up` is not available yet.

Frontend references: [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
and [HTMX](https://htmx.org/docs/).
