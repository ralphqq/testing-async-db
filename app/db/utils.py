"""
Helper database functions

Functions:
    create_tables(engine, tables)
    delete_tables(engine, tables)
"""
from aiopg.sa import Engine
from sqlalchemy.schema import CreateTable, DropTable


async def create_tables(engine: Engine, tables: list) -> None:
    """Creates all tables in tables list."""
    async with engine.acquire() as conn:
        for table in tables:
            create_table_stmt = CreateTable(table.__table__)
            await conn.execute(create_table_stmt)


async def delete_tables(engine: Engine, tables: list) -> None:
    """Deletes tables included in list."""
    async with engine.acquire() as conn:
        for table in reversed(tables):
            delete_table_stmt = DropTable(table.__table__)
            await conn.execute(delete_table_stmt)
