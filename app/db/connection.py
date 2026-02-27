import asyncpg
from app.core.config import settings

pool = None


async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(settings.DATABASE_URL)
    return pool


async def close_pool():
    global pool
    if pool:
        await pool.close()
        pool = None
