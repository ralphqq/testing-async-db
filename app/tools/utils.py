"""
Helper/Utility functions
"""
from urllib.parse import urlparse


def get_domain_name(url):
    """Returns netloc from parsed URL."""
    try:
        p = urlparse(url)
        return p.netloc
    except Exception as e:
        pass
