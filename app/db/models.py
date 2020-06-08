"""
Model definitions for database tables

Classes:
    Base
    CommonFieldsMixin
    ScraperInfo
    ScrapedItem
    Source
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class CommonFieldsMixin:
    """To be sub-classed by models."""

    id = Column(Integer, primary_key=True)


class ScraperInfo(CommonFieldsMixin, Base):
    __tablename__ = 'scraper_info'

    name = Column(String(128), nullable=False, unique=True, index=True)
    site_name = Column(String(128), nullable=False)
    site_url = Column(String(2048), nullable=False)
    scraped_items = relationship(
        'ScrapedItem',
        backref='source_scraper',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Scraper {self.name}>'


class ScrapedItem(CommonFieldsMixin, Base):
    __tablename__ = 'scraped_item'

    title = Column(String(256), nullable=False, index=True)
    url = Column(String(2048), nullable=False, unique=True)
    source_id = Column(Integer, ForeignKey('source.id'))
    scraper_id = Column(Integer, ForeignKey('scraper_info.id'))
    scraped_ts = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ScrapedItem {self.title}>'


class Source(CommonFieldsMixin, Base):
    __tablename__ = 'source'

    domain = Column(String(2048), nullable=False, index=True, unique=True)
    pages = relationship(
        'ScrapedItem',
        backref='website',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Source {self.domain}>'