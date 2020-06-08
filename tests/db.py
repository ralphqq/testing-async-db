from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DATABASE


TEST_DB = dict(DATABASE)

engine = create_engine(URL(**TEST_DB))
Session = scoped_session(sessionmaker(bind=engine))
