"""pytest configuration"""

import pytest
from pingurl import persistance


@pytest.fixture(scope="function", autouse=True)
def reset_persistance():
    """Resets global variables between tests"""
    persistance.pings = {}
    persistance.watched_urls = {}
    persistance.next_id = 0
