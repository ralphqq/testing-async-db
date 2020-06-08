import pytest
from sqlalchemy.exc import IntegrityError

from app.db.models import ScrapedItem, ScraperInfo, Source


class ModelTestMixin:
    """Includes helper/convenience methods."""

    def init_table(self, model, data, session):
        """Inserts initial data to table."""
        session.bulk_insert_mappings(model, data)
        session.commit()


class TestScraperInfo(ModelTestMixin):

    def test_scraper_info_creation(self, db_session_with_json_data):
        db, data = db_session_with_json_data
        scrapers = data['scraper_info']
        self.init_table(ScraperInfo, scrapers, db)
        count = db.query(ScraperInfo).count()
        assert count == len(scrapers)

    def test_avoids_duplicate_scraper_name(self, db_session_with_json_data):
        db, data = db_session_with_json_data
        scrapers = data['scraper_info']
        self.init_table(ScraperInfo, scrapers, db)
        existing_scraper = scrapers[0]
        with pytest.raises(IntegrityError):
            info = ScraperInfo(**existing_scraper)
            db.add(info)
            db.commit()

    def test_enforces_non_nullable_fields(self, db_session):
        with pytest.raises(IntegrityError):
            info = ScraperInfo()
            db_session.add(info)
            db_session.commit()
