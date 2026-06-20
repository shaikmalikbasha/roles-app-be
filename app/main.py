import app.models  # noqa: F401 — registers ORM models with Base.metadata
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.database import create_all_tables

    await create_all_tables()
    yield


app = FastAPI(title="Roles App", lifespan=lifespan)


@app.get("/")
async def health_check():
    return {"status": "ok"}
