import pytest

from app.tools.utils import get_domain_name


class TestGetDomainName:

    @pytest.mark.parametrize(
        'url,domain_name',
        [
            ('www.google.com/incomplete.html', ''),
            ('blog.stackoverflow.com', ''),
            ('not-a-url', ''),
        ]
    )
    def test_invalid_urls_return_empty_str(self, url, domain_name):
        assert get_domain_name(url) == domain_name

    def test_exceptions_cause_domain_getter_to_return_none(self, monkeypatch):
        def mocked_urlparse():
            raise ValueError
        monkeypatch.setattr('app.tools.utils.urlparse', mocked_urlparse)
        result = get_domain_name('https://www.google.com')
        assert result is None
