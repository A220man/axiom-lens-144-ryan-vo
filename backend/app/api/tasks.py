"""Task management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, UTC
import uuid

from app.api.auth import get_current_user, TokenData

router = APIRouter()

# In-memory store (production: use database)
_tasks: dict[str, dict] = {}


class TaskCreate(BaseModel):
    goal: str = Field(..., min_length=1, max_length=5000)
    device_id: Optional[str] = None
    model: Optional[str] = None


class TaskResponse(BaseModel):
    id: str
    goal: str
    device_id: Optional[str]
    model: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    result: Optional[dict] = None

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user: TokenData = Depends(get_current_user)):
    task_id = str(uuid.uuid4())
    now = datetime.now(UTC)
    task_data = {
        "id": task_id,
        "goal": task.goal,
        "device_id": task.device_id,
        "model": task.model,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
        "result": None,
        "owner_id": current_user.sub,
    }
    _tasks[task_id] = task_data
    return TaskResponse(**task_data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: TokenData = Depends(get_current_user)):
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = _tasks[task_id]
    if task.get("owner_id") != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")
    return TaskResponse(**task)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(limit: int = 50, offset: int = 0, current_user: TokenData = Depends(get_current_user)):
    tasks = [t for t in _tasks.values() if t.get("owner_id") == current_user.sub]
    tasks.sort(key=lambda t: t["created_at"], reverse=True)
    return [TaskResponse(**t) for t in tasks[offset:offset + limit]]
