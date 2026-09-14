# FairShare

FairShare is a local expense-splitting application. The frontend is a static Bootstrap UI and the backend is a Django JSON API.

## Project structure

```text
02-development/
├── api/                 Django API views, services, and mock repository
├── fairshare/           Django project configuration
├── frontend/            Static frontend application
├── tests/               Backend endpoint tests
├── openapi.yaml         API contract
├── manage.py             Django management entry point
└── pyproject.toml        uv dependencies
```

## Requirements

- Windows PowerShell or WSL
- Python 3.11+
- The repository includes a local uv executable at `..\.tools\uv\uv.exe` when running from this directory.

## Run the backend

Open a PowerShell window and run from `02-development`:

```powershell
cd D:\courses\ai_devtools_dtalks\ai_dev_tools_2026\02-development
$env:UV_CACHE_DIR = Join-Path (Get-Location) ".uv-cache"
& ..\.tools\uv\uv.exe sync
& ..\.tools\uv\uv.exe run python manage.py runserver 127.0.0.1:8000
```

The backend is available at:

```text
http://127.0.0.1:8000
```

The root URL does not serve an HTML page. Use the API URLs under `/api/`, for example:

```text
http://127.0.0.1:8000/api/auth/me/
```

When not logged in, this endpoint correctly returns `401 Unauthorized`.

## Run the frontend

Keep the backend running and open a second PowerShell window:

```powershell
cd D:\courses\ai_devtools_dtalks\ai_dev_tools_2026\02-development\frontend
python -m http.server 8001
```

Open the application at:

```text
http://127.0.0.1:8001/
```

The frontend calls the backend on port `8000` through `frontend/api.js`, using the same hostname as the page (`localhost` or `127.0.0.1`). Keep the hostname consistent in the browser URL and backend URL so session and CSRF cookies work correctly. The backend allows the local frontend origin and handles session cookies and CSRF tokens.

## Demo login

```text
Username: demo
Password: demo
```

You can also choose **Create an account** from the login page.

## Run tests

Run this from `02-development` in a separate PowerShell window:

```powershell
cd D:\courses\ai_devtools_dtalks\ai_dev_tools_2026\02-development
$env:UV_CACHE_DIR = Join-Path (Get-Location) ".uv-cache"
& ..\.tools\uv\uv.exe run python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 10 tests
OK
```

Run Django's system check with:

```powershell
& ..\.tools\uv\uv.exe run python manage.py check
```

## Database

The backend uses SQLAlchemy through the repository in `api/repository.py`. Local development defaults to a real SQLite database at:

```text
fairshare.sqlite3
```

The SQLAlchemy models and repository are database-agnostic. Change the `DATABASE_URL` environment variable to use another SQLAlchemy-supported database without changing the API views or frontend contract. For example:

```powershell
$env:DATABASE_URL = "sqlite:///fairshare.sqlite3"
```

For PostgreSQL, install the appropriate SQLAlchemy driver and use a URL such as:

```text
postgresql+psycopg://user:password@localhost/fairshare
```

Endpoint tests set `DATABASE_URL=sqlite:///:memory:` so test data is isolated from the local development database.

## Stopping the servers

In each server terminal, press:

```text
Ctrl+C
```

The backend uses port `8000` and the frontend uses port `8001`. If a port is already in use, stop the old server first or start one of the services on another port.

## API contract

The complete API definition is in [openapi.yaml](openapi.yaml). It documents authentication, CSRF initialization, expense creation, listing, detail, deletion, validation errors, and authorization behavior.
