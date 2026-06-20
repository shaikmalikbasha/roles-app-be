from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import AsyncSessionLocal

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def liveness() -> dict:
    return {"status": "ok"}


@router.get("/db")
async def db_probe() -> dict:
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError:
        return {"status": "degraded", "database": "unavailable"}
