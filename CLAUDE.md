# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Roles App Backend is a lightweight Role-Based Access Control (RBAC) service built with **FastAPI** and **SQLite** (via async SQLAlchemy 2.0). Users inherit permissions through assigned roles.

## Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Lint
ruff check .

# Format
ruff format .

# Run tests
pytest

# Run a single test file
pytest tests/path/to/test_file.py

# Run a single test by name
pytest -k "test_name"
```

## Architecture

The project uses a strict 4-layer architecture with clear separation of concerns:

```
HTTP Request
    ↓
app/api/          — Thin route handlers; delegate to services, inject dependencies
    ↓
app/services/     — Business logic, validation, authorization decisions, transactions
    ↓
app/repositories/ — Database access only; CRUD and query abstraction; no business logic
    ↓
app/models/       — SQLAlchemy ORM models (SQLite via aiosqlite)
```

**Supporting modules:**
- `app/schemas/` — Pydantic v2 models for request/response validation and serialization
- `app/core/` — App configuration (`config.py`), JWT + password hashing (`security.py`), DB session (`database.py`)
- `app/dependencies/` — FastAPI `Depends()` factories for auth and permission enforcement

## Key Patterns

**Permission enforcement** via dependency injection:
```python
@router.post("/users", dependencies=[Depends(require_permission("user:create"))])
```

**All database operations must be async** (SQLAlchemy async session + aiosqlite driver).

**Never return password hashes** in API responses — schemas must exclude password fields.

**Password hashing**: Argon2 only. **Token signing**: JWT with secret key.

## Standards

### Python
- Use `X | None` not `Optional[X]`; use `X | Y` unions throughout
- All async functions must be `async def`; never mix sync DB calls in async context
- Type-annotate all function signatures (parameters + return type)
- No `print()` — use Python `logging` if observability is needed

### REST
- `POST` → 201, `DELETE` → 204 (no body), `GET`/`PATCH` → 200
- Never return a password hash or raw secret in any response
- Error shape is always `{"detail": "..."}` (FastAPI default — don't override it)
- Route paths are plural nouns: `/users`, `/roles`, `/permissions`

### FastAPI
- Route handlers are thin — delegate all logic to the service layer
- Inject DB session via `Depends(get_db)`, never instantiate sessions in routes
- Enforce permissions with `dependencies=[Depends(require_permission("resource:action"))]`

### SQLAlchemy
- All queries are async; use `await session.execute(...)` not `.execute(...)` directly
- Always `await session.commit()` in the service layer, not the repository layer
- Repositories return ORM model instances; services convert to schemas before returning

### Pydantic
- Response schemas must never include `password` or `hashed_password` fields
- Use `model_config = ConfigDict(from_attributes=True)` on all response schemas

## Data Model

- `User` ↔ `Role`: many-to-many
- `Role` ↔ `Permission`: many-to-many
- Users inherit permissions transitively through roles
- Permission naming convention: `resource:action` (e.g., `user:create`, `role:delete`)

## API Surface

| Module | Endpoints |
|---|---|
| Auth | `POST /auth/login`, `GET /auth/me` |
| Users | `POST/GET /users`, `GET/PATCH/DELETE /users/{id}` |
| Roles | `POST/GET /roles`, `GET/PATCH/DELETE /roles/{id}` |
| Permissions | `POST/GET /permissions`, `GET/PATCH/DELETE /permissions/{id}` |
| User↔Role | `POST/DELETE /users/{user_id}/roles/{role_id}` |
| Role↔Permission | `POST/DELETE /roles/{role_id}/permissions/{permission_id}` |

---

## Development Workflow

This project is built **one GitHub issue at a time**. Do not implement multiple issues in a single session unless explicitly asked.

### Issue Tracker

All 12 issues live at: https://github.com/shaikmalikbasha/roles-app-be/issues

| # | Title | Status |
|---|-------|--------|
| [#1](https://github.com/shaikmalikbasha/roles-app-be/issues/1) | Add missing auth dependencies to requirements.txt | ✅ Done |
| [#2](https://github.com/shaikmalikbasha/roles-app-be/issues/2) | Scaffold app/ directory, package init files, and main.py | ✅ Done |
| [#3](https://github.com/shaikmalikbasha/roles-app-be/issues/3) | Implement async SQLAlchemy database session | ✅ Done |
| [#4](https://github.com/shaikmalikbasha/roles-app-be/issues/4) | Implement config settings and security utilities | ✅ Done |
| [#5](https://github.com/shaikmalikbasha/roles-app-be/issues/5) | Define User, Role, Permission ORM models with M2M relationships | ⬜ Next |
| [#6](https://github.com/shaikmalikbasha/roles-app-be/issues/6) | Define Pydantic v2 schemas | ⬜ Todo |
| [#7](https://github.com/shaikmalikbasha/roles-app-be/issues/7) | Implement async CRUD repositories | ⬜ Todo |
| [#8](https://github.com/shaikmalikbasha/roles-app-be/issues/8) | Implement FastAPI auth and permission dependencies | ⬜ Todo |
| [#9](https://github.com/shaikmalikbasha/roles-app-be/issues/9) | Implement authentication endpoints | ⬜ Todo |
| [#10](https://github.com/shaikmalikbasha/roles-app-be/issues/10) | Implement user CRUD endpoints | ⬜ Todo |
| [#11](https://github.com/shaikmalikbasha/roles-app-be/issues/11) | Implement role and permission CRUD endpoints | ⬜ Todo |
| [#12](https://github.com/shaikmalikbasha/roles-app-be/issues/12) | Write async integration test suite | ⬜ Todo |

### Branch Naming Convention

```
<type>/<short-slug>

setup/    — dependency or config changes
infra/    — scaffolding, project structure
core/     — foundational modules (database, config, security)
feature/  — business features (routes, services)
tests/    — test suite additions
fix/      — bug fixes
```

### PR Workflow (follow every time)

1. Pull latest `main`: `git pull`
2. Create a branch: `git checkout -b <type>/<slug>`
3. Implement the issue
4. Lint: `ruff check . && ruff format .`
5. Commit with a message that references the issue: `Closes #N`
6. Push: `git push -u origin <branch>`
7. Open PR via `gh pr create`
8. Close the GitHub issue with a comment summarising what was done

### After Each Merge

Update the Issue Tracker table above — move the completed issue to ✅ Done and set the next one to ⬜ Next. Keep this file committed to `main` so the next session starts with accurate state.
