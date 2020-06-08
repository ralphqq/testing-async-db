import json
import os

import pytest

from settings import BASE_DIR


DATA_DIR = os.path.join(BASE_DIR, 'tests/data')
DATA_FILES = [
    'scraped_items.json',
    'scraper_info.json',
    'sources.json',
]


@pytest.fixture(scope='function')
def db_session():
    """Sets up and tears down database session."""
    from app.db.models import Base
    from tests.db import engine, Session

    # Create all tables and yield a scoped session instance
    Base.metadata.create_all(engine)
    session = Session()
    yield session

    # Close the session and drop all tables
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def db_session_with_json_data(db_session):
    """Loads data from JSON files and yields a session.

    Returns:
        tuple: (db_session, data)
    """
    data = {}
    for datafile in DATA_FILES:
        fpath = os.path.join(DATA_DIR, datafile)
        fname, _ = os.path.splitext(datafile)
        with open(fpath, 'r', encoding='utf-8') as f:
            data[fname] = json.load(f)
    return db_session, data
