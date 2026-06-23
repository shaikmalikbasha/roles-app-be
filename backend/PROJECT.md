# Roles App Backend

## Overview

Roles App Backend is a lightweight Role-Based Access Control (RBAC) service built with FastAPI.

The application provides:

- User Management
- Role Management
- Permission Management
- Authentication
- Authorization

The service can be used as a standalone RBAC system or integrated into larger applications such as:

- Hospital ERP
- School Management System
- CRM
- HRMS
- SaaS Platforms

---

## Tech Stack

### Backend

- FastAPI
- Python 3.12+

### Database

- SQLite
- SQLAlchemy 2.0 Async
- aiosqlite

### Authentication

- JWT Access Tokens
- OAuth2 Password Bearer
- Argon2 Password Hashing

### Validation

- Pydantic v2

---

## Core Concepts

### User

Represents an authenticated application user.

#### Examples

- malik.shaik@example.com
- admin@example.com
- doctor@example.com

A user can have multiple roles.

---

### Role

Represents a collection of permissions.

#### Examples

- Admin
- Doctor
- Nurse
- Receptionist

A role can have multiple permissions.

---

### Permission

Represents a single action.

#### Examples

```text
user:create
user:view
user:update
user:delete

role:create
role:view
role:update
role:delete
```

Permissions are assigned to roles.

Users inherit permissions through assigned roles.

---

## Relationships

### User ↔ Role

**Many-to-Many**

```text
User
 ├─ Admin
 └─ Manager
```

---

### Role ↔ Permission

**Many-to-Many**

```text
Admin
 ├─ user:create
 ├─ user:view
 ├─ user:update
 └─ user:delete
```

---

## Authentication Flow

### Login

**POST** `/auth/login`

#### Request

```json
{
  "email": "admin@example.com",
  "password": "secret"
}
```

#### Response

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

### Current User

**GET** `/auth/me`

#### Response

```json
{
  "id": "...",
  "email": "admin@example.com",
  "roles": [
    "Admin"
  ],
  "permissions": [
    "user:create",
    "user:view"
  ]
}
```

---

## API Modules

### Auth

| Method | Endpoint |
|----------|----------|
| POST | `/auth/login` |
| GET | `/auth/me` |

---

### Users

| Method | Endpoint |
|----------|----------|
| POST | `/users` |
| GET | `/users` |
| GET | `/users/{user_id}` |
| PATCH | `/users/{user_id}` |
| DELETE | `/users/{user_id}` |

---

### Roles

| Method | Endpoint |
|----------|----------|
| POST | `/roles` |
| GET | `/roles` |
| GET | `/roles/{role_id}` |
| PATCH | `/roles/{role_id}` |
| DELETE | `/roles/{role_id}` |

---

### Permissions

| Method | Endpoint |
|----------|----------|
| POST | `/permissions` |
| GET | `/permissions` |
| GET | `/permissions/{permission_id}` |
| PATCH | `/permissions/{permission_id}` |
| DELETE | `/permissions/{permission_id}` |

---

### User Roles

| Method | Endpoint |
|----------|----------|
| POST | `/users/{user_id}/roles/{role_id}` |
| DELETE | `/users/{user_id}/roles/{role_id}` |

---

### Role Permissions

| Method | Endpoint |
|----------|----------|
| POST | `/roles/{role_id}/permissions/{permission_id}` |
| DELETE | `/roles/{role_id}/permissions/{permission_id}` |

---

## Project Structure

```text
app/
│
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── roles.py
│   └── permissions.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── role.py
│   └── permission.py
│
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── role.py
│   └── permission.py
│
├── repositories/
│   ├── user_repository.py
│   ├── role_repository.py
│   └── permission_repository.py
│
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   ├── role_service.py
│   └── permission_service.py
│
├── dependencies/
│   ├── auth.py
│   └── permissions.py
│
├── main.py
│
└── requirements.txt
```

---

## Authorization Strategy

### Authentication

- JWT Access Token

### Authorization

```text
User
  ↓
Roles
  ↓
Permissions
```

Permission checks should be implemented through FastAPI dependencies.

Example:

```python
Depends(require_permission("user:create"))
```

---

## Architectural Guidelines

### Repository Layer

Responsible for:

- Database access
- CRUD operations
- Query abstraction

Repositories should not contain business logic.

---

### Service Layer

Responsible for:

- Business rules
- Validation
- Authorization decisions
- Transaction orchestration

Services should use repositories.

---

### API Layer

Responsible for:

- Request handling
- Response serialization
- Dependency injection
- Authentication and authorization integration

API routes should remain thin and delegate work to services.

---

## Security Requirements

- Passwords must be hashed using Argon2.
- JWT tokens must be signed with a secret key.
- Protected routes require authentication.
- Sensitive operations require permission checks.
- Never return password hashes in API responses.

---

## Future Enhancements

- Refresh Tokens
- Role Hierarchy
- Permission Groups
- Multi-Tenant Support
- Audit Logs
- Soft Deletes
- PostgreSQL Support
- Alembic Migrations

---

## Development Principles

- Use async SQLAlchemy throughout the project.
- Follow FastAPI dependency injection patterns.
- Use Pydantic v2 schemas for request and response models.
- Keep business logic inside services.
- Keep database logic inside repositories.
- Favor explicit typing.
- Maintain clear separation of concerns.
- Write clean, testable, modular code.