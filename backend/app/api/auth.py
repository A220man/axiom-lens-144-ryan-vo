"""Authentication endpoints (OIDC Keycloak)."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import secrets
import httpx

from app.core.config import settings

router = APIRouter()

# In-memory state store (production: use Redis)
_oidc_states: dict[str, dict] = {}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.get("/login")
async def login(request: Request):
    """Initiate OIDC authorization code flow with PKCE."""
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = code_verifier  # S256 would hash this; simplified for demo

    _oidc_states[state] = {
        "code_verifier": code_verifier,
        "redirect_uri": str(request.url_for("callback")),
    }

    auth_url = (
        f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/auth"
        f"?client_id={settings.keycloak_client_id}"
        f"&response_type=code"
        f"&scope=openid profile email"
        f"&redirect_uri={_oidc_states[state]['redirect_uri']}"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=plain"
    )
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def callback(code: str, state: str):
    """Handle OIDC callback, exchange code for tokens."""
    if state not in _oidc_states:
        raise HTTPException(status_code=400, detail="Invalid state")

    stored = _oidc_states.pop(state)
    token_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.keycloak_client_id,
                "client_secret": settings.keycloak_client_secret,
                "redirect_uri": stored["redirect_uri"],
                "code_verifier": stored["code_verifier"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    token_data = await resp.json()
    return TokenResponse(**token_data)


@router.post("/logout")
async def logout():
    """Logout endpoint (client clears tokens)."""
    return {"message": "Logged out"}
