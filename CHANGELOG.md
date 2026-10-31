# Changelog

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

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
