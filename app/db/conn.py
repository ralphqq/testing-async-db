"""
Utilities for working with database layer

Classes:
    DBConnection
"""
from aiopg.sa import create_engine

from app.db.utils import create_tables


class DBConnection:
    """Handles db connection and interface."""

    def __init__(self) -> None:
        self.engine = None

    async def init(self, config: dict, tables: list = None) -> None:
        """Creates db engine and tables."""
        engine = await create_engine(
            database=config['database'],
            user=config['username'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
        self.engine = engine
        if tables:
            await create_tables(engine, tables)

    async def close(self) -> None:
        """Closes db engine."""
        self.engine.close()
