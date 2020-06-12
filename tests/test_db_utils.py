from aiopg.sa import create_engine
import pytest
from sqlalchemy.sql import text

from app.db.models import Base, MODELS_LIST
from app.db.utils import create_tables, delete_tables
from tests.db import DATABASE


class TestDBUtils:

    @pytest.fixture
    async def engine(self):
        config = dict(DATABASE)

        db_engine = await create_engine(
            database=config['database'],
            user=config['username'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
        yield db_engine

        # Clean up db and close engine
        async with db_engine.acquire() as conn:
            await conn.execute("DROP SCHEMA public CASCADE")
            await conn.execute("CREATE SCHEMA public")
            await conn.execute("GRANT ALL ON SCHEMA public TO postgres")
            await conn.execute("GRANT ALL ON SCHEMA public TO public")
        db_engine.close()

    @pytest.mark.asyncio
    async def test_create_tables_function(self, engine):
        await create_tables(engine=engine, tables=MODELS_LIST)

        results = None
        async with engine.acquire() as conn:
            query = text(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                """
            )
            rows = await conn.execute(query)
            results = await rows.fetchall()

        fetched_tablenames = [res[0] for res in results]
        for table in MODELS_LIST:
            assert table.__tablename__ in fetched_tablenames
