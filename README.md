# Axiom Lens | Ryan Vo | AI & Machine Learning

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


**Axiom Lens** is an Android automation platform that turns natural-language instructions into reliable on-device workflows. It automates end-to-end tasks, captures structured execution traces, and integrates with AI coding assistants. The core AI/ML engine uses multimodal models for perception, planning, action, and verification — running locally via OpenAI-compatible servers (Gemma 4 E4B, Ollama, vLLM) or cloud providers.

## Problem
Mobile UI automation is brittle: element selectors break, screens vary, and scripts don't generalize. Axiom Lens replaces brittle selectors with a vision-language agent that sees the screen, plans actions, executes them, and verifies results — all from a natural-language goal.

## AI/ML Approach
- **Perception**: Screenshots + UI hierarchy → multimodal LLM (Gemma 4 E4B, Gemini, GPT-4o)
- **Planning**: Structured tool-calling loop (plan → act → verify) with bounded context
- **Grounding**: Visual grounding via image tokens; coordinate mapping from UI hierarchy
- **Verification**: Explicit `checked`/`enabled` state exposure for labeled controls (fixes #187)

## Intended User
Mobile QA engineers, AI researchers, and developers who need reliable, reproducible Android automation without maintaining fragile XPath/accessibility-id scripts.

## Quick Start

```bash
# 1. Clone and enter
cd axiom-lens-144-ryan-vo

# 2. Backend setup
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt

# 3. Frontend setup
cd frontend && npm install && cd ..

# 4. Start services (Keycloak, backend, frontend)
docker compose up -d

# 5. Run tests
.venv/bin/pytest backend/tests -v
cd frontend && npm test && cd ..
```

## Architecture

```mermaid
graph TD
    UI[Web Console] --> API[FastAPI Backend]
    API --> Auth[Keycloak OIDC]
    API --> LLM[LLM Adapters]
    API --> Device[Android Device Driver]
    LLM --> Local[Local OpenAI-compatible\n(Gemma 4 E4B, Ollama)]
    LLM --> Cloud[Cloud Providers\n(OpenAI, Anthropic, Gemini)]
    Device --> ADB[ADB / WebUSB Bridge]
```

## AI/ML Evaluation

```bash
# Reproducible evaluation on AndroidWorld subset
.venv/bin/python -m pytest backend/tests/test_automation_engine.py::test_task_completion -v
```

**Data Provenance**: Synthetic UI hierarchies + captured Android Settings traces (no PII).
**Baseline**: Rule-based selector automation (0% generalization to unseen screens).
**Measured**: Task completion rate, steps-to-goal, self-termination accuracy.
**Failure Cases**: Hallucinated elements, termination loops, infeasibility detection.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /api/v1/tasks | Submit automation task |
| GET | /api/v1/tasks/{id} | Get task status/results |
| GET | /api/v1/devices | List connected devices |
| POST | /api/v1/auth/login | Initiate OIDC login |
| GET | /api/v1/auth/callback | OIDC callback |

## Provider Configuration

| Provider | Env Vars | Models |
|----------|----------|--------|
| OpenAI-compatible | `LLM_PROVIDER=custom`, `LLM_API_KEY`, `LLM_BASE_URL` | Any (Gemma, Llama, etc.) |
| OpenAI | `LLM_PROVIDER=openai`, `LLM_API_KEY` | gpt-4o, gpt-4o-mini |
| Anthropic | `LLM_PROVIDER=anthropic`, `LLM_API_KEY` | claude-3.5-sonnet |
| Gemini | `LLM_PROVIDER=gemini`, `LLM_API_KEY` | gemini-1.5-flash |
| Ollama | `LLM_PROVIDER=ollama`, `LLM_BASE_URL` | Any local model |

## SSO/SAML Setup
Keycloak supports SAML identity brokering. Import `docs/keycloak-realm.json`, configure your SAML IdP as an identity provider in the realm, and map attributes to Keycloak roles (`viewer`, `operator`, `admin`).

## Security Limitations
- Local demo mode binds to 127.0.0.1 only; refuses to start in production without real OIDC
- ADB protocol is unencrypted; use SSH tunnels or the browser-side WebUSB bridge (planned)
- LLM keys never leave the backend; no client-side key exposure

## License
MIT © Ryan Vo <ryandtvo@gmail.com>
