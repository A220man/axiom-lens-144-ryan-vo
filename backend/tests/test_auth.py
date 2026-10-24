"""Authentication tests."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from unittest.mock import AsyncMock, patch


@pytest.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_login_redirects(client: AsyncClient):
    response = await client.get("/api/v1/auth/login", follow_redirects=False)
    assert response.status_code == 307
    assert "location" in response.headers
    # Check it redirects to the Keycloak auth endpoint
    assert "realms/axiom-lens/protocol/openid-connect/auth" in response.headers["location"]


@pytest.mark.asyncio
async def test_callback_invalid_state(client: AsyncClient):
    response = await client.get("/api/v1/auth/callback?code=test&state=invalid")
    assert response.status_code == 400
    assert "Invalid state" in response.json()["detail"]


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_callback_success(mock_post, client: AsyncClient):
    # First, initiate login to create state
    login_resp = await client.get("/api/v1/auth/login", follow_redirects=False)
    location = login_resp.headers["location"]
    # Extract state from location
    import urllib.parse
    parsed = urllib.parse.urlparse(location)
    params = urllib.parse.parse_qs(parsed.query)
    state = params["state"][0]

    # Mock token exchange
    mock_resp = AsyncMock()
    mock_resp.status_code = 200
    mock_resp.json = AsyncMock(return_value={
        "access_token": "test-token",
        "token_type": "bearer",
        "expires_in": 300,
    })
    mock_post.return_value = mock_resp

    response = await client.get(f"/api/v1/auth/callback?code=auth-code&state={state}")
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "test-token"
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"
