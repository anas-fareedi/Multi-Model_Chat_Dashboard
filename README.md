# Multi-Model Chat Dashboard

A web-based dashboard to interact with and compare multiple conversational models (LLMs or chat APIs) from one unified interface. The project provides a configurable frontend UI and backend orchestration so you can add, query, and inspect responses from different models side-by-side.

Key goals:
- Fast, side-by-side comparison of multiple chat models
- Centralized management of model credentials and settings
- Simple extensibility to add new models or evaluation metrics

## Features
- Add and manage multiple models (API-based or self-hosted)
- Single chat UI that sends the same prompt to selected models
- Response comparison (timestamps, latencies, model metadata)
- Conversation history per model and cross-model session view
- Pluggable adapters for new model providers

## Contents
- /frontend — (optional) Single-page app for the dashboard UI
- /backend  — (optional) API server that handles model adapters, sessions, and persistence
- /adapters — (optional) Example connectors for third-party model APIs
- docker-compose.yml — (optional) Example development/production stacks

(If your repository structure differs, update the paths above.)

## Prerequisites
- Docker & Docker Compose (recommended) OR
- Node.js >= 16 (for typical React/Vite/Next frontends)
- Python >= 3.9 or Node.js for the backend depending on implementation
- API keys for the models/providers you want to use (OpenAI, Anthropic, local LLM endpoints, etc.)

## Quick Start (Docker)
1. Copy and configure environment variables:
   - Create a `.env` file at repo root (example below)
2. Start services:
   docker compose up --build
3. Visit the dashboard:
   - http://localhost:3000 (or configured frontend port)

## Quick Start (Local development)
1. Clone the repository
   git clone https://github.com/anas-fareedi/Multi-Model_Chat_Dashboard.git
   cd Multi-Model_Chat_Dashboard

2. Backend (example)
   - Install dependencies (adjust for your stack):
     - Python: python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt
     - Node: cd backend && npm install
   - Run:
     - Python: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
     - Node: cd backend && npm run dev

3. Frontend (example)
   - cd frontend
   - npm install
   - npm run dev
   - Open http://localhost:3000

Adjust ports and commands to match the repository's tooling.

## Environment variables (.env example)
Update with provider credentials and preferred settings.

# Example .env
OPENAI_API_KEY=sk-xxxx
ANTHROPIC_API_KEY=claude-xxxx
MODEL_REGISTRY={"openai":"gpt-4o","anthropic":"claude-2"}
BACKEND_HOST=http://localhost:8000
FRONTEND_PORT=3000
DATABASE_URL=sqlite:///./db.sqlite3

Note: Use secure storage for production secrets.

## Adding a new model provider
1. Create an adapter following the project's adapter contract (check /adapters or docs).
2. Register the adapter with the backend (config file or environment).
3. Add the model metadata via the admin UI or config to surface it in the dashboard.

Suggested adapter responsibilities:
- Authenticate to provider
- Perform request/response shaping (input prompts, parameters)
- Normalize response metadata (latency, token usage where available)

## Persisting Conversations
This repo may include simple persistence (SQLite/Postgres) or a stateless mode. Configure DATABASE_URL in your .env. If using persistence:
- Run migrations (if present), e.g., alembic upgrade head or prisma migrate deploy

## Security & Rate Limits
- Never commit API keys to source control.
- Observe provider rate limits; add retries/backoff and pooling in adapters where appropriate.
- Sanitize user inputs if you expose the dashboard publicly.

## Contributing
Contributions are welcome.
- Open an issue to propose features or report bugs.
- Fork the repo, create a branch, add tests, and open a pull request.
- Follow the existing code style and include documentation for new adapters.

## Troubleshooting
- If a model fails to respond, check provider credentials and network access.
- For CORS issues, confirm backend CORS settings allow the frontend origin.
- Check logs for adapter-specific error messages and provider rate-limit responses.

## Roadmap / Ideas
- Built-in evaluation metrics (BLEU, ROUGE, human ranking)
- Side-by-side conversation diffing and export
- Authentication and multi-tenant support
- Plugin system for custom visualizations

## License
Specify a license for this repository (e.g., MIT). Add a LICENSE file at the repo root.

## Contact
Maintainer: anas-fareedi
GitHub: https://github.com/anas-fareedi

If anything in this README needs to be made specific to the repository (detected tech stack, exact start commands, env var names), tell me which stack or share a list of files and I will tailor it to be exact and minimal.
