"""Axiom Lens - Android automation with AI/ML core."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import health, tasks, devices, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


def create_app() -> FastAPI:
    app = FastAPI(
        title="Axiom Lens",
        version="1.0.0",
        description="Android automation platform with AI/ML core",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, tags=["health"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
    app.include_router(devices.router, prefix="/api/v1/devices", tags=["devices"])

    return app


app = create_app()
