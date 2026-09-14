from django.http import HttpResponse

ALLOWED_ORIGINS = {"http://127.0.0.1:8001", "http://localhost:8001"}


class LocalCorsMiddleware:
    """Minimal local-development CORS support for the static frontend."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = HttpResponse(status=204) if request.method == "OPTIONS" else self.get_response(request)
        origin = request.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
            response["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
            response["Vary"] = "Origin"
        return response
