import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.postgres import PostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from agents import build_graph

@asynccontextmanager
async def lifespan(app):
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    pool = ConnectionPool(
        conninfo=database_url,
        min_size=1,
        max_size=10,
        kwargs={
            "row_factory": dict_row,
            "autocommit": True
        },
        open=False
    )

    try:
        pool.open(wait=True)

        checkpointer = PostgresSaver(pool)
        checkpointer.setup()

        app.state.graph = build_graph(checkpointer)

        yield

    finally:
        pool.close()