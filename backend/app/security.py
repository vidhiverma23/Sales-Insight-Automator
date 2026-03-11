"""Security utilities: rate limiting, API key validation, security headers."""

from fastapi import Request, HTTPException, Security
from fastapi.security import APIKeyHeader
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address)

# --- API Key Auth (optional) ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Validate API key if one is configured in settings."""
    settings = get_settings()
    if settings.API_KEY and api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return api_key
