# Backend — CLAUDE.md

FastAPI + SQLite (async SQLAlchemy 2.0) RBAC REST API.

## Commands

```bash
cd backend

python run.py                        # dev server
uvicorn app.main:app --reload        # equivalent

ruff check .                         # lint
ruff format .                        # format

pytest                               # all tests
pytest tests/path/to/test_file.py   # single file
pytest -k "test_name"               # single test
```

> `.venv` lives inside `backend/`. Recreate: `python -m venv .venv && pip install -r requirements.txt`

---

## Architecture

Domain-driven structure — each feature owns its router, service, repository, model, and schemas.

```
app/
  auth/         — router.py, service.py, schemas.py
  users/        — router.py, service.py, repository.py, model.py, schemas.py
  roles/        — router.py, service.py, repository.py, model.py, schemas.py
  permissions/  — router.py, service.py, repository.py, model.py, schemas.py
  health/       — router.py
  core/         — config.py, database.py, security.py, base_model.py, base_repository.py
  dependencies/ — auth.py, permissions.py
  main.py
```

**4-layer contract:**
```
router.py      — thin handlers, Depends injection
service.py     — business logic, commit here
repository.py  — DB access only, inherits BaseRepository[T]
model.py       — SQLAlchemy ORM (inherits BaseMixin + Base)
```

**Core utilities:**
- `base_model.py` — `BaseMixin`: `id`, `created_at`, `updated_at`, `is_deleted`
- `base_repository.py` — `BaseRepository[T]`: `get_by_id`, `get_all`, `create`, `update`, `delete`
- `security.py` — JWT encode/decode, Argon2 password hashing

---

## Standards

### Python
- `X | None` not `Optional[X]`; `X | Y` unions
- All DB functions `async def`; never mix sync DB calls in async context
- Type-annotate all signatures (params + return)
- No `print()` — use `logging`

### REST
- `POST` → 201, `DELETE` → 204, `GET`/`PATCH` → 200
- Never return password hash or raw secret
- Error shape: `{"detail": "..."}` (FastAPI default)
- Route paths are plural nouns: `/users`, `/roles`, `/permissions`

### FastAPI
- Thin route handlers — all logic in service layer
- `Depends(get_db)` for sessions, never instantiate manually
- `dependencies=[Depends(require_permission("resource:action"))]` for auth

### SQLAlchemy
- `await session.execute(...)` always
- `await session.commit()` in service layer, not repository
- Repositories return ORM instances; services convert to schemas

### Pydantic
- Response schemas never include `password` / `hashed_password`
- `model_config = ConfigDict(from_attributes=True)` on all response schemas

---

## Data Model

- `User` ↔ `Role`: many-to-many
- `Role` ↔ `Permission`: many-to-many
- Permission naming: `resource:action` (e.g. `user:create`, `role:delete`)

## API Surface

| Module | Endpoints |
|--------|-----------|
| Auth | `POST /auth/login`, `GET /auth/me` |
| Users | `POST/GET /users`, `GET/PATCH/DELETE /users/{id}` |
| Roles | `POST/GET /roles`, `GET/PATCH/DELETE /roles/{id}` |
| Permissions | `POST/GET /permissions`, `GET/PATCH/DELETE /permissions/{id}` |
| User↔Role | `POST/DELETE /users/{user_id}/roles/{role_id}` |
| Role↔Permission | `POST/DELETE /roles/{role_id}/permissions/{permission_id}` |
