# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

skeleton

## Roadmap

### skeleton — FastAPI/React skeleton with install instructions and tests

Status: done

Acceptance:
- Backend FastAPI app runs with health endpoint
- Frontend React+TypeScript+Vite builds and serves
- Docker Compose brings up backend, frontend, Keycloak
- Basic pytest and vitest tests pass
- README has install/run/test steps

Implementation: `backend/app/main.py`, `backend/app/api/health.py`, `backend/app/api/auth.py`, `backend/app/api/tasks.py`, `backend/app/api/devices.py`, `backend/app/core/config.py`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/pages/Dashboard.tsx`, `frontend/src/pages/Tasks.tsx`, `frontend/src/pages/Devices.tsx`, `frontend/src/pages/Login.tsx`, `frontend/src/pages/Callback.tsx`, `frontend/src/hooks/useAuth.tsx`, `frontend/src/api/client.ts`, `compose.yaml`

Tests: `backend/tests/test_health.py`, `backend/tests/test_auth.py`, `backend/tests/test_tasks.py`, `backend/tests/test_devices.py`, `frontend/src/__tests__/App.test.tsx`, `frontend/src/__tests__/Dashboard.test.tsx`, `frontend/src/__tests__/Tasks.test.tsx`

### auth — OIDC Keycloak authentication with SPA PKCE flow

Status: planned

Acceptance:
- Login redirects to Keycloak
- Callback exchanges code for tokens
- Tokens stored in memory (not localStorage)
- API endpoints require valid bearer token
- Logout clears session

### llm-adapters — Multi-provider LLM adapters (OpenAI-compatible, Anthropic, Gemini, Ollama)

Status: planned

Acceptance:
- Provider resolution from config
- Structured output via tool calling
- Bounded timeouts and redacted errors
- Keys only server-side

### automation-engine — Core automation engine with device observation and action execution

Status: planned

Acceptance:
- Device connection and screenshot capture
- UI hierarchy parsing
- Tap/swipe/text input actions
- Task execution loop with perception->planning->action->verification

### web-console — Web console for task submission and monitoring

Status: planned

Acceptance:
- Task submission form
- Real-time execution log
- Device selection
- Results display with screenshots

