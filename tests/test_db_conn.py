import pytest
from unittest.mock import patch

from app.db.conn import DBConnection
from app.db.models import MODELS_LIST
from tests.db import DATABASE
from tests.utils import MockedCoroutine


class TestDBConnection:

    @pytest.fixture
    def mocked_create_tables(self):
        patcher = patch(
            'app.db.conn.create_tables',
            new_callable=MockedCoroutine
        )
        yield patcher.start()
        patcher.stop()

    @pytest.mark.asyncio
    async def test_db_conn_init_without_tables(self, mocked_create_tables):
        db = DBConnection()
        await db.init(config=DATABASE)
        assert db.engine is not None
        assert not mocked_create_tables.called

    @pytest.mark.asyncio
    async def test_db_conn_init_with_tables(self, mocked_create_tables):
        db = DBConnection()
        await db.init(config=DATABASE, tables=MODELS_LIST)
        assert db.engine is not None
        assert mocked_create_tables.called

    @pytest.mark.asyncio
    async def test_closing_db_connection_engine(self, mocked_create_tables):
        db = DBConnection()
        await db.init(config=DATABASE)
        await db.close()
        with pytest.raises(RuntimeError):
            conn = await db.engine.acquire()
