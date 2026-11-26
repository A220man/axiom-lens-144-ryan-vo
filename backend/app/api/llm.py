"""LLM provider resolution endpoints.

Exposes which LLM adapter is resolved from configuration without ever
returning secrets (API keys are never included in responses).
"""

from fastapi import APIRouter

from app.services.llm_adapters import (
    create_adapter,
    validate_provider_config,
)

router = APIRouter()


@router.get("/provider")
async def get_provider() -> dict:
    """Return the resolved LLM provider and adapter from configuration.

    Resolution is derived from ``settings`` (LLM_PROVIDER, LLM_MODEL,
    LLM_BASE_URL). The API key is intentionally never read into the
    response.
    """
    validation = validate_provider_config()

    adapter_name: str | None = None
    resolution_error: str | None = None
    try:
        adapter = create_adapter()
        adapter_name = type(adapter).__name__
    except ValueError as exc:
        # Redact: only the message, which never contains the key.
        resolution_error = str(exc)

    return {
        "provider": validation["provider"],
        "adapter": adapter_name,
        "is_valid": validation["is_valid"],
        "warnings": validation["warnings"],
        "resolution_error": resolution_error,
    }
