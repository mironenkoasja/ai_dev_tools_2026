SECRET_KEY = "fairshare-local-development-key"
DEBUG = True
ROOT_URLCONF = "fairshare.urls"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = []
MIDDLEWARE = [
    "api.middleware.LocalCorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8001", "http://localhost:8001"]
USE_TZ = True
TIME_ZONE = "UTC"
ROOT_URLCONF = "fairshare.urls"
