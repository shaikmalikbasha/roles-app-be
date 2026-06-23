# Roles App

A lightweight Role-Based Access Control (RBAC) system — FastAPI backend + React SPA admin UI.

## Structure

```
backend/   FastAPI + SQLite REST API (Python)
frontend/  React + Vite + TanStack SPA admin UI (TypeScript, Bun)
```

## Quick start

**Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # fill in SECRET_KEY
python run.py               # http://localhost:8000
```

**Frontend**
```bash
cd frontend
bun install
bun run dev                 # http://localhost:5173
```

See [CLAUDE.md](CLAUDE.md) for full architecture and development workflow.
