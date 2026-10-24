"""Task management tests."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post("/api/v1/tasks", json={"goal": "Open Settings"})
    assert response.status_code == 201
    data = response.json()
    assert data["goal"] == "Open Settings"
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient):
    create_resp = await client.post("/api/v1/tasks", json={"goal": "Test task"})
    task_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["goal"] == "Test task"


@pytest.mark.asyncio
async def test_get_nonexistent_task(client: AsyncClient):
    response = await client.get("/api/v1/tasks/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    await client.post("/api/v1/tasks", json={"goal": "Task 1"})
    await client.post("/api/v1/tasks", json={"goal": "Task 2"})

    response = await client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_task_pagination(client: AsyncClient):
    for i in range(5):
        await client.post("/api/v1/tasks", json={"goal": f"Task {i}"})

    response = await client.get("/api/v1/tasks?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = await client.get("/api/v1/tasks?limit=2&offset=2")
    assert len(response.json()) == 2
