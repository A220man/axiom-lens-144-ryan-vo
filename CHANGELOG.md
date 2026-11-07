# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint
### Added (llm-adapters feature)
- Multi-provider LLM adapter layer (OpenAI-compatible, Anthropic, Gemini, Ollama)
- Provider resolution from config via factory function
- Structured output via tool/function calling for all providers
- Bounded request timeouts (default 30s)
- Server-side API key handling (keys never leave backend)
- LLM service with lifespan integration for resource cleanup
- Unit tests for all adapters, factory, and service

### Changed
- Updated `backend/app/main.py` to close LLM service on shutdown
- Updated PLAN.md and STATUS.md for llm-adapters in_progress

### Verified
- Backend: New test file `test_llm_adapters.py` created (tests not yet run)
- Feature implementation complete per acceptance criteria except error redaction
Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Added (auth feature)
- OIDC Keycloak authentication with SPA PKCE flow (S256 code challenge)
- JWT bearer token validation dependency (`get_current_user`) for protected endpoints
- Task and device endpoints now require authentication
- Frontend auth context with sessionStorage token storage (not localStorage)
- Axios interceptors for automatic Authorization header attachment and 401 redirect
- Improved error handling in Tasks and Devices pages with user-facing error messages

### Changed
- Backend tests updated to use authenticated client fixture (`auth_client`)
- PKCE upgraded from plain to S256 method
- Token decode uses dummy key with `verify_signature=False` for demo

### Verified
- Backend: 17/17 pytest tests pass (including new unauthorized access tests)
- Frontend: 6/6 vitest tests pass

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-31

### Added
- Initial FastAPI/React skeleton with Docker Compose
- Health check endpoint
- Basic project structure (backend/api/services/models/core, frontend/src)
- pytest and vitest test configuration
- Keycloak OIDC integration placeholder
- Multi-provider LLM adapter framework

### Fixed
- TypeScript errors in frontend test files (mock types)
- Unused imports/variables in Callback.tsx
- datetime.utcnow() deprecation warning (use datetime.now(UTC))
- pytest-asyncio event_loop fixture deprecation warning

### Verified
- Backend: 15/15 pytest tests pass, 0 warnings
- Frontend: 6/6 vitest tests pass
- Frontend build: TypeScript compilation + Vite production build succeed
- Docker Compose configuration valid
