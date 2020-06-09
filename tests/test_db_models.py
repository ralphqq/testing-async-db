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
            (ScrapedItem, 'scraped_items', 'url'),
            (ScraperInfo, 'scraper_info', 'name'),
            (Source, 'sources', 'domain'),
        ],
        ids=['scraped_item', 'scraper', 'source']
    )
    def init_table(self, request, db_session, json_data):
        """Inserts initial data to table.

        Returns:
            tuple: (db_session, model, data, unique_field)
        """
        model, name, unique_field = request.param
        data = json_data[name]

        if name == 'scraped_items':
            # Remove 'scraper' and 'source' items
            data = _remove_items(data, ['source', 'scraper'])

        db_session.bulk_insert_mappings(model, data)
        db_session.commit()
        return db_session, model, data, unique_field

    def test_new_row_insertion(self, init_table):
        session, model, data, _ = init_table
        count = session.query(model).count()
        assert count == len(data)

    def test_avoids_duplicate_rows(self, init_table):
        session, model, data, _ = init_table
        existing_row = data[0]
        with pytest.raises(IntegrityError):
            item = model(**existing_row)
            session.add(item)
            session.commit()

    def test_enforces_non_nullable_fields(self, init_table):
        session, model, data, _ = init_table
        with pytest.raises(IntegrityError):
            item = model()
            session.add(item)
            session.commit()

    def test_if_repr_works(self, init_table):
        session, model, data, _ = init_table
        row = session.query(model).first()
        assert repr(row)

    def test_get_or_create_new_row(self, init_table):
        session, model, data, field = init_table

        # Simulate new data row by modifying
        #  fields in existing rows with unique constraint
        new_row = dict(data[0])
        new_row[field] = 'newvalue'

        new_item, is_new = model.get_or_create(session=session, **new_row)
        session.commit()
        new_count = session.query(model).count()

        assert new_count == len(data) + 1
        assert isinstance(new_item, model)
        assert is_new

    def test_get_or_create_old_row(self, init_table):
        session, model, data, field = init_table
        old_row = data[0]
        old_item, is_new = model.get_or_create(session=session, **old_row)
        count = session.query(model).count()
        assert count == len(data)
        assert isinstance(old_item, model)
        assert not is_new
