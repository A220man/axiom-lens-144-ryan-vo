# Changelog

## 1.2.0 — work-in-progress checkpoint

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
