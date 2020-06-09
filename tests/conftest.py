import json
import os

import pytest

from app.db.models import Base
from settings import BASE_DIR
from tests.db import engine, delete_rows, Session


DATA_DIR = os.path.join(BASE_DIR, 'tests/data')
DATA_FILES = [
    'scraped_items.json',
    'scraper_info.json',
    'sources.json',
]


@pytest.fixture(scope='class')
def init_db():
    """Creates and drops db."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def db_session(init_db):
    """Sets up and tears down db session."""
    session = Session()
    yield session
    session.rollback()
    session.close()
    delete_rows(db_engine=engine, base_obj=Base)


@pytest.fixture(scope='class')
def json_data():
    """Loads data from JSON files and returns it as `dict`."""
    data = {}

    for datafile in DATA_FILES:
        fpath = os.path.join(DATA_DIR, datafile)
        fname, _ = os.path.splitext(datafile)

        with open(fpath, 'r', encoding='utf-8') as f:
            data[fname] = json.load(f)

    return data
