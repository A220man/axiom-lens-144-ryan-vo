"""Tests for the LLM provider resolution endpoint."""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from app.main import create_app
from app.core.config import settings


@pytest.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_provider_endpoint_custom(client: AsyncClient):
    with patch.object(settings, "llm_provider", "custom"), \
         patch.object(settings, "llm_api_key", "synthetic-key"), \
         patch.object(settings, "llm_base_url", "http://localhost:8080/v1"), \
         patch.object(settings, "llm_model", "test-model"):
        response = await client.get("/api/v1/llm/provider")

    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "custom"
    assert data["adapter"] == "OpenAICompatibleAdapter"
    assert data["is_valid"] is True
    assert data["resolution_error"] is None
    # Secret must never leak into the response body.
    assert "synthetic-key" not in response.text


@pytest.mark.asyncio
async def test_provider_endpoint_unknown_provider(client: AsyncClient):
    with patch.object(settings, "llm_provider", "mystery"):
        response = await client.get("/api/v1/llm/provider")

    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "mystery"
    assert data["adapter"] is None
    assert data["is_valid"] is False
    assert data["resolution_error"] is not None
    assert "Unknown LLM provider" in data["resolution_error"]
