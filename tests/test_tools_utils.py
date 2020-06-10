import pytest

from app.tools.utils import get_domain_name


class TestGetDomainName:

    @pytest.fixture
    def item_source_domain_pairs(self, scraped_item_source_data):
        return [
            (itm['url'], src['domain']) for itm, src in scraped_item_source_data
        ]

    def test_domain_getter_util(self, item_source_domain_pairs):
        for url, domain_name in item_source_domain_pairs:
            result = get_domain_name(url)
            assert result == domain_name

    @pytest.mark.parametrize('url', [
        'www.google.com/incomplete.html',
        'blog.stackoverflow.com',
        'not-a-url',
    ])
    def test_invalid_urls_return_empty_str(self, url):
        assert get_domain_name(url) == ''

    def test_exceptions_cause_domain_getter_to_return_none(self, monkeypatch):
        def mocked_urlparse():
            raise ValueError
        monkeypatch.setattr('app.tools.utils.urlparse', mocked_urlparse)
        result = get_domain_name('https://www.google.com')
        assert result is None
