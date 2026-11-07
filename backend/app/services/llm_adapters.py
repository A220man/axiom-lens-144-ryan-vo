"""Multi-provider LLM adapters with structured output support."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional
import json
import httpx
from pydantic import BaseModel, Field

from app.core.config import settings


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    tool_calls: list[dict] | None = None
    usage: dict | None = None
    raw: Any = None


class LLMAdapter(ABC):
    """Abstract base class for LLM adapters."""

    @abstractmethod
    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | dict | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Generate a completion."""
        pass

    @abstractmethod
    async def close(self):
        """Close any resources."""
        pass


class OpenAICompatibleAdapter(LLMAdapter):
    """Adapter for OpenAI-compatible APIs (OpenAI, vLLM, Ollama, etc.)."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=self.timeout,
            )
        return self._client

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | dict | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        client = self._get_client()

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if tools:
            payload["tools"] = tools
            if tool_choice:
                payload["tool_choice"] = tool_choice

        response = await client.post("/chat/completions", json=payload)
        response.raise_for_status()
        data = response.json()

        choice = data["choices"][0]
        message = choice["message"]

        tool_calls = message.get("tool_calls")
        if tool_calls:
            # Normalize tool calls to standard format
            tool_calls = [
                {
                    "id": tc["id"],
                    "type": tc["type"],
                    "function": {
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"],
                    },
                }
                for tc in tool_calls
            ]

        return LLMResponse(
            content=message.get("content") or "",
            tool_calls=tool_calls,
            usage=data.get("usage"),
            raw=data,
        )

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()


class AnthropicAdapter(LLMAdapter):
    """Adapter for Anthropic API."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://api.anthropic.com",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                timeout=self.timeout,
            )
        return self._client

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | dict | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        client = self._get_client()

        # Convert OpenAI-style messages to Anthropic format
        system_message = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                anthropic_messages.append({"role": msg["role"], "content": msg["content"]})

        payload = {
            "model": self.model,
            "messages": anthropic_messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 4096,
        }
        if system_message:
            payload["system"] = system_message
        if tools:
            # Convert OpenAI-style tools to Anthropic format
            payload["tools"] = [
                {
                    "name": t["function"]["name"],
                    "description": t["function"].get("description", ""),
                    "input_schema": t["function"].get("parameters", {}),
                }
                for t in tools
            ]
            if tool_choice:
                if tool_choice == "auto":
                    payload["tool_choice"] = {"type": "auto"}
                elif isinstance(tool_choice, dict) and tool_choice.get("type") == "function":
                    payload["tool_choice"] = {"type": "tool", "name": tool_choice["function"]["name"]}

        response = await client.post("/v1/messages", json=payload)
        response.raise_for_status()
        data = response.json()

        # Convert Anthropic response to standard format
        content_blocks = data.get("content", [])
        text_content = ""
        tool_calls = []

        for block in content_blocks:
            if block["type"] == "text":
                text_content += block["text"]
            elif block["type"] == "tool_use":
                tool_calls.append({
                    "id": block["id"],
                    "type": "function",
                    "function": {
                        "name": block["name"],
                        "arguments": json.dumps(block["input"]),
                    },
                })

        return LLMResponse(
            content=text_content,
            tool_calls=tool_calls if tool_calls else None,
            usage={
                "prompt_tokens": data.get("usage", {}).get("input_tokens", 0),
                "completion_tokens": data.get("usage", {}).get("output_tokens", 0),
                "total_tokens": data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0),
            },
            raw=data,
        )

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()


class GeminiAdapter(LLMAdapter):
    """Adapter for Google Gemini API."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://generativelanguage.googleapis.com",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | dict | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        client = self._get_client()

        # Convert messages to Gemini format
        contents = []
        system_instruction = None
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = {"parts": [{"text": msg["content"]}]}
            elif msg["role"] == "user":
                contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
            elif msg["role"] == "assistant":
                contents.append({"role": "model", "parts": [{"text": msg["content"]}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens or 4096,
            },
        }
        if system_instruction:
            payload["systemInstruction"] = system_instruction

        if tools:
            payload["tools"] = [{
                "functionDeclarations": [
                    {
                        "name": t["function"]["name"],
                        "description": t["function"].get("description", ""),
                        "parameters": t["function"].get("parameters", {}),
                    }
                    for t in tools
                ]
            }]

        url = f"/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        # Convert Gemini response to standard format
        candidates = data.get("candidates", [])
        if not candidates:
            return LLMResponse(content="", raw=data)

        candidate = candidates[0]
        content = candidate.get("content", {})
        parts = content.get("parts", [])

        text_content = ""
        tool_calls = []

        for part in parts:
            if "text" in part:
                text_content += part["text"]
            elif "functionCall" in part:
                fc = part["functionCall"]
                tool_calls.append({
                    "id": fc.get("id", "call_" + str(hash(str(fc)))),
                    "type": "function",
                    "function": {
                        "name": fc["name"],
                        "arguments": json.dumps(fc.get("args", {})),
                    },
                })

        usage = data.get("usageMetadata", {})
        return LLMResponse(
            content=text_content,
            tool_calls=tool_calls if tool_calls else None,
            usage={
                "prompt_tokens": usage.get("promptTokenCount", 0),
                "completion_tokens": usage.get("candidatesTokenCount", 0),
                "total_tokens": usage.get("totalTokenCount", 0),
            },
            raw=data,
        )

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()


def create_adapter() -> LLMAdapter:
    """Factory function to create the appropriate LLM adapter based on config."""
    provider = settings.llm_provider.lower()

    if provider in ("custom", "openai", "ollama", "vllm"):
        return OpenAICompatibleAdapter(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            model=settings.llm_model,
        )
    elif provider == "anthropic":
        return AnthropicAdapter(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    elif provider == "gemini":
        return GeminiAdapter(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")


class LLMService:
    """High-level service for LLM interactions."""

    def __init__(self):
        self._adapter: LLMAdapter | None = None

    @property
    def adapter(self) -> LLMAdapter:
        if self._adapter is None:
            self._adapter = create_adapter()
        return self._adapter

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | dict | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Generate a completion using the configured adapter."""
        return await self.adapter.complete(
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def close(self):
        if self._adapter:
            await self._adapter.close()
            self._adapter = None


# Global service instance
llm_service = LLMService()
