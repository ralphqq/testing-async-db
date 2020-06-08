import pytest
from sqlalchemy.exc import IntegrityError

from app.db.models import ScrapedItem, ScraperInfo, Source


class TestScraperInfo:

    @pytest.fixture(scope='function')
    def init_table(self, db_session_with_json_data):
        """Inserts initial data to table."""
        session, data = db_session_with_json_data
        scrapers = data['scraper_info']
        session.bulk_insert_mappings(ScraperInfo, scrapers)
        session.commit()
        return session, scrapers

    def test_scraper_info_creation(self, init_table):
        session, scrapers = init_table
        count = session.query(ScraperInfo).count()
        assert count == len(scrapers)

    def test_avoids_duplicate_scraper_name(self, init_table):
        session, scrapers = init_table
        existing_scraper = scrapers[0]
        with pytest.raises(IntegrityError):
            info = ScraperInfo(**existing_scraper)
            session.add(info)
            session.commit()

    def test_enforces_non_nullable_fields(self, db_session):
        with pytest.raises(IntegrityError):
            info = ScraperInfo()
            db_session.add(info)
            db_session.commit()
