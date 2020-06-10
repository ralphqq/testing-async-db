import pytest

from app.tools.utils import get_domain_name


@pytest.mark.parametrize(
    'url,domain_name',
    [
        (
            'http://www.overcomingbias.com/2020/06/no-recent-automation-revolution.html',
            'www.overcomingbias.com'
        ),
        (
            'https://blog.rust-lang.org/inside-rust/2020/06/08/new-inline-asm.html',
            'blog.rust-lang.org'
        ),
        ('not-a-url', ''),
    ]
)
def test_domain_name_getter(url, domain_name):
    assert get_domain_name(url) == domain_name


def test_exceptions_cause_domain_getter_to_return_none(monkeypatch):
    def mocked_urlparse():
        raise ValueError
    monkeypatch.setattr('app.tools.utils.urlparse', mocked_urlparse)
    result = get_domain_name('https://www.google.com')
    assert result is None
