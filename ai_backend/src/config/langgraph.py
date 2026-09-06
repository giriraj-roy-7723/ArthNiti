import os
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

DATABASE_URL = os.getenv("DATABASE_URL")

pool: AsyncConnectionPool | None = None
checkpointer: AsyncPostgresSaver | None = None


async def init_langgraph():
    global pool, checkpointer

    conninfo = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

    pool = AsyncConnectionPool(
        conninfo=conninfo,
        min_size=1,
        max_size=5,
        kwargs={
            "autocommit": True,
            "prepare_threshold": None,
        },
        open=False,
    )

    await pool.open()

    checkpointer = AsyncPostgresSaver(pool)

    await checkpointer.setup()


async def close_langgraph():
    global pool, checkpointer

    if pool:
        await pool.close()
        pool = None
        checkpointer = None
