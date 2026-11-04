"""Pytest configuration for backend tests."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from jose import jwt
from datetime import datetime, UTC, timedelta


TEST_USER_ID = "test-user-123"


def create_test_token(user_id: str = TEST_USER_ID) -> str:
    """Create a test JWT token (no signature verification in demo)."""
    payload = {
        "sub": user_id,
        "preferred_username": "testuser",
        "email": "test@example.com",
        "realm_access": {"roles": ["user"]},
        "exp": datetime.now(UTC) + timedelta(hours=1),
        "iat": datetime.now(UTC),
    }
    # No key needed since verify_signature=False in auth
    return jwt.encode(payload, "test-secret", algorithm="HS256")


TEST_TOKEN = create_test_token()


@pytest.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_client():
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    ) as ac:
        yield ac
