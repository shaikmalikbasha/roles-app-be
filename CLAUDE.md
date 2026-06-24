# CLAUDE.md

## Repo Layout

Monorepo with two halves:

| Directory | Stack | Purpose |
|-----------|-------|---------|
| `backend/` | FastAPI + SQLite (async SQLAlchemy 2.0) | RBAC REST API |
| `frontend/` | React + Vite + TypeScript (Bun) | SPA admin UI |

> Each half has its own `CLAUDE.md` with stack-specific architecture, commands, and standards.

---

## Development Workflow

Build **one GitHub issue at a time**. Do not implement multiple issues in a single session unless explicitly asked.

**Issue tracker:** https://github.com/shaikmalikbasha/roles-app-be/issues  
Run `gh issue list` to see open issues. Current next issue is marked ⬜ Next below.

| # | Title | Status |
|---|-------|--------|
| [#12](https://github.com/shaikmalikbasha/roles-app-be/issues/12) | Write async integration test suite | ⬜ Todo |
| [#39](https://github.com/shaikmalikbasha/roles-app-be/issues/39) | Build app layout shell with sidebar navigation | ✅ Done |
| [#40](https://github.com/shaikmalikbasha/roles-app-be/issues/40) | Add shared UI components — DataTable, Dialog, Select, Toast | ✅ Done |
| [#41](https://github.com/shaikmalikbasha/roles-app-be/issues/41) | Build Permissions management page | ⬜ Next |
| [#42](https://github.com/shaikmalikbasha/roles-app-be/issues/42) | Build Roles management page | ⬜ Todo |
| [#43](https://github.com/shaikmalikbasha/roles-app-be/issues/43) | Build Users management page | ⬜ Todo |

Use `/done` after each issue to ship: lint → build → commit → push → PR → close issue → update this table.

---

## Branch Naming

```
feature/   — business features
fix/       — bug fixes
infra/     — scaffolding, project structure
core/      — foundational modules
setup/     — dependency or config changes
tests/     — test suite additions
```
