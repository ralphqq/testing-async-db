from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DATABASE


TEST_DB = dict(DATABASE)

engine = create_engine(URL(**TEST_DB))
Session = scoped_session(sessionmaker(bind=engine))


def delete_rows(db_engine, base_obj):
    """Deletes data in tables without dropping the schema."""
    connection = db_engine.connect()
    with connection.begin() as trans:
        for table in reversed(base_obj.metadata.sorted_tables):
            connection.execute(table.delete())
        trans.commit()
    connection.close()
