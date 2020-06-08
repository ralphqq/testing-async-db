import pytest
from sqlalchemy.exc import IntegrityError

from app.db.models import ScrapedItem, ScraperInfo, Source


def _remove_items(data, keys):
    """Removes given keys for all items in data."""
    for row in data:
        for k in keys:
            if k in row:
                row.pop(k)
    return data


class TestModelBasics:

    @pytest.fixture(
        scope='function',
        params=[
            (ScrapedItem, 'scraped_items'),
            (ScraperInfo, 'scraper_info'),
            (Source, 'sources'),
        ],
        ids=['scraped_item', 'scraper', 'source']
    )
    def init_table(self, request, db_session, json_data):
        """Inserts initial data to table.

        Returns:
            tuple: (db_session, model, data)
        """
        model, name = request.param
        data = json_data[name]

        if name == 'scraped_items':
            # Remove 'scraper' and 'source' items
            data = _remove_items(data, ['source', 'scraper'])

        db_session.bulk_insert_mappings(model, data)
        db_session.commit()
        return db_session, model, data

    def test_new_row_insertion(self, init_table):
        session, model, data = init_table
        count = session.query(model).count()
        assert count == len(data)

    def test_avoids_duplicate_rows(self, init_table):
        session, model, data = init_table
        existing_row = data[0]
        with pytest.raises(IntegrityError):
            item = model(**existing_row)
            session.add(item)
            session.commit()

    def test_enforces_non_nullable_fields(self, init_table):
        session, model, data = init_table
        with pytest.raises(IntegrityError):
            item = model()
            session.add(item)
            session.commit()

    def test_if_repr_works(self, init_table):
        session, model, data = init_table
        row = session.query(model).first()
        assert repr(row)
