"""Device management tests."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_list_devices_empty(client: AsyncClient):
    response = await client.get("/api/v1/devices")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_connect_device(client: AsyncClient):
    response = await client.post("/api/v1/devices/emulator-5554/connect")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "emulator-5554"
    assert data["status"] == "connected"


@pytest.mark.asyncio
async def test_get_device(client: AsyncClient):
    await client.post("/api/v1/devices/emulator-5554/connect")
    response = await client.get("/api/v1/devices/emulator-5554")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "emulator-5554"


@pytest.mark.asyncio
async def test_disconnect_device(client: AsyncClient):
    await client.post("/api/v1/devices/emulator-5554/connect")
    response = await client.post("/api/v1/devices/emulator-5554/disconnect")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "disconnected"


@pytest.mark.asyncio
async def test_get_nonexistent_device(client: AsyncClient):
    response = await client.get("/api/v1/devices/nonexistent")
    assert response.status_code == 404
