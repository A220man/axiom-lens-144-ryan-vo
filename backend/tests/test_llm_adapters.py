"""Tests for LLM adapters."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.llm_adapters import (
    LLMResponse,
    OpenAICompatibleAdapter,
    AnthropicAdapter,
    GeminiAdapter,
    create_adapter,
    LLMService,
    llm_service,
)
from app.core.config import settings


class TestOpenAICompatibleAdapter:
    """Tests for OpenAI-compatible adapter."""

    @pytest.fixture
    def adapter(self):
        return OpenAICompatibleAdapter(
            api_key="test-key",
            base_url="http://localhost:8080/v1",
            model="test-model",
        )

    @pytest.mark.asyncio
    async def test_complete_success(self, adapter):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "Hello, world!",
                    "tool_calls": None,
                },
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        adapter._client = mock_client

        result = await adapter.complete([
            {"role": "user", "content": "Hello"},
        ])

        assert isinstance(result, LLMResponse)
        assert result.content == "Hello, world!"
        assert result.tool_calls is None
        assert result.usage["total_tokens"] == 15

    @pytest.mark.asyncio
    async def test_complete_with_tool_calls(self, adapter):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"location": "San Francisco"}',
                        },
                    }],
                },
                "finish_reason": "tool_calls",
            }],
            "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30},
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        adapter._client = mock_client

        result = await adapter.complete([
            {"role": "user", "content": "What's the weather?"},
        ], tools=[{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {"type": "object", "properties": {"location": {"type": "string"}}},
            },
        }])

        assert result.tool_calls is not None
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0]["function"]["name"] == "get_weather"

    @pytest.mark.asyncio
    async def test_close(self, adapter):
        mock_client = AsyncMock()
        adapter._client = mock_client
        await adapter.close()
        mock_client.aclose.assert_called_once()


class TestAnthropicAdapter:
    """Tests for Anthropic adapter."""

    @pytest.fixture
    def adapter(self):
        return AnthropicAdapter(
            api_key="test-key",
            model="claude-3-sonnet",
        )

    @pytest.mark.asyncio
    async def test_complete_success(self, adapter):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [
                {"type": "text", "text": "Hello, world!"},
            ],
            "usage": {"input_tokens": 10, "output_tokens": 5},
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        adapter._client = mock_client

        result = await adapter.complete([
            {"role": "user", "content": "Hello"},
        ])

        assert isinstance(result, LLMResponse)
        assert result.content == "Hello, world!"
        assert result.usage["total_tokens"] == 15

    @pytest.mark.asyncio
    async def test_complete_with_tool_calls(self, adapter):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [
                {"type": "tool_use", "id": "call_123", "name": "get_weather", "input": {"location": "SF"}},
            ],
            "usage": {"input_tokens": 20, "output_tokens": 10},
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        adapter._client = mock_client

        result = await adapter.complete([
            {"role": "user", "content": "What's the weather?"},
        ], tools=[{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {"type": "object", "properties": {"location": {"type": "string"}}},
            },
        }])

        assert result.tool_calls is not None
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0]["function"]["name"] == "get_weather"


class TestGeminiAdapter:
    """Tests for Gemini adapter."""

    @pytest.fixture
    def adapter(self):
        return GeminiAdapter(
            api_key="test-key",
            model="gemini-1.5-flash",
        )

    @pytest.mark.asyncio
    async def test_complete_success(self, adapter):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Hello, world!"}],
                },
                "finishReason": "STOP",
            }],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5, "totalTokenCount": 15},
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        adapter._client = mock_client

        result = await adapter.complete([
            {"role": "user", "content": "Hello"},
        ])

        assert isinstance(result, LLMResponse)
        assert result.content == "Hello, world!"
        assert result.usage["total_tokens"] == 15

    @pytest.mark.asyncio
    async def test_complete_with_function_calls(self, adapter):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [
                        {"functionCall": {"name": "get_weather", "args": {"location": "SF"}}},
                    ],
                },
                "finishReason": "STOP",
            }],
            "usageMetadata": {"promptTokenCount": 20, "candidatesTokenCount": 10, "totalTokenCount": 30},
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        adapter._client = mock_client

        result = await adapter.complete([
            {"role": "user", "content": "What's the weather?"},
        ], tools=[{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {"type": "object", "properties": {"location": {"type": "string"}}},
            },
        }])

        assert result.tool_calls is not None
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0]["function"]["name"] == "get_weather"


class TestCreateAdapter:
    """Tests for adapter factory."""

    def test_create_openai_compatible(self):
        with patch.object(settings, "llm_provider", "custom"):
            with patch.object(settings, "llm_api_key", "test-key"):
                with patch.object(settings, "llm_base_url", "http://localhost:8080/v1"):
                    with patch.object(settings, "llm_model", "test-model"):
                        adapter = create_adapter()
                        assert isinstance(adapter, OpenAICompatibleAdapter)

    def test_create_ollama(self):
        with patch.object(settings, "llm_provider", "ollama"):
            with patch.object(settings, "llm_api_key", "test-key"):
                with patch.object(settings, "llm_base_url", "http://localhost:11434/v1"):
                    with patch.object(settings, "llm_model", "llama3"):
                        adapter = create_adapter()
                        assert isinstance(adapter, OpenAICompatibleAdapter)

    def test_create_anthropic(self):
        with patch.object(settings, "llm_provider", "anthropic"):
            with patch.object(settings, "llm_api_key", "test-key"):
                with patch.object(settings, "llm_model", "claude-3-sonnet"):
                    adapter = create_adapter()
                    assert isinstance(adapter, AnthropicAdapter)

    def test_create_gemini(self):
        with patch.object(settings, "llm_provider", "gemini"):
            with patch.object(settings, "llm_api_key", "test-key"):
                with patch.object(settings, "llm_model", "gemini-1.5-flash"):
                    adapter = create_adapter()
                    assert isinstance(adapter, GeminiAdapter)

    def test_unknown_provider_raises(self):
        with patch.object(settings, "llm_provider", "unknown"):
            with pytest.raises(ValueError, match="Unknown LLM provider"):
                create_adapter()


class TestLLMService:
    """Tests for high-level LLM service."""

    @pytest.mark.asyncio
    async def test_service_uses_adapter(self):
        mock_adapter = AsyncMock()
        mock_adapter.complete.return_value = LLMResponse(content="test")
        service = LLMService()
        service._adapter = mock_adapter

        result = await service.complete([{"role": "user", "content": "hello"}])

        assert result.content == "test"
        mock_adapter.complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_service_close(self):
        mock_adapter = AsyncMock()
        service = LLMService()
        service._adapter = mock_adapter

        await service.close()

        mock_adapter.close.assert_called_once()
        assert service._adapter is None
