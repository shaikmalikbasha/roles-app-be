from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.core.middleware import RequestIDMiddleware
from app.health.router import router as health_router
from app.permissions.router import router as permissions_router
from app.roles.router import router as roles_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.database import create_all_tables

    await create_all_tables()
    yield


app = FastAPI(title="Roles App", lifespan=lifespan)

app.add_middleware(RequestIDMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        # Add your frontend URLs here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(permissions_router)
