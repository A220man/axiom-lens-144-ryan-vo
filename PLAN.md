# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

skeleton

## Roadmap

### skeleton — FastAPI/React skeleton with install instructions and tests

Status: in_progress

Acceptance:
- Backend FastAPI app runs with health endpoint
- Frontend React+TypeScript+Vite builds and serves
- Docker Compose brings up backend, frontend, Keycloak
- Basic pytest and vitest tests pass
- README has install/run/test steps

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

