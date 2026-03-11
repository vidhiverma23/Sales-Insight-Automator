"""FastAPI application entry point with security middleware."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config import get_settings
from app.security import limiter
from app.routers import upload

settings = get_settings()


# --- Security Headers Middleware ---
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


# --- App Factory ---
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "🚀 **Sales Insight Automator** by Rabbitt AI\n\n"
        "Upload sales data (CSV/XLSX), get an AI-generated executive brief "
        "delivered straight to your inbox.\n\n"
        "### How it works\n"
        "1. **Upload** a `.csv` or `.xlsx` file\n"
        "2. **Provide** a recipient email\n"
        "3. **Receive** a professional sales insight report via email\n\n"
        "### Security\n"
        "- Rate limited (5 requests/minute per IP)\n"
        "- Optional API key authentication via `X-API-Key` header\n"
        "- Input validation & file size limits"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# --- Middleware ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(upload.router)


# --- Root ---
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API info."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/health",
    }
