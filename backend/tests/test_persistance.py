"""tests for persistance.py"""
from datetime import datetime
import pytest
from pingurl import persistance
from pingurl.models import WatchedUrl


def test_delete_watched_url_value_error():
    """test for delete wrong input type"""
    with pytest.raises(ValueError) as excinfo:
        persistance.delete_watched_url("foo")
    assert str(excinfo.value) == "url_id must be an integer"


def test_delete_watched_url_not_found_error():
    """test for delete url not found error"""
    with pytest.raises(persistance.WatchedUrlNotFoundError) as excinfo:
        persistance.delete_watched_url(1)
    assert str(excinfo.value) == "url_id not found"


def test_delete_watched_url():
    """test for successful deletion of url_id"""
    next_id = 0
    time = datetime.fromisoformat("2023-11-16T12:55:07+00:00")
    persistance.watched_urls[next_id] = WatchedUrl(
        activate_at=time,
        force=True,
        url="http://www.example.com",
        url_id=next_id,
        period_sec=1,
    )
    persistance.delete_watched_url(0)
    assert 0 not in persistance.watched_urls
