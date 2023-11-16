"""Test get_watch_url"""
import pytest
from pingurl import persistance
from pingurl.persistance import WatchedUrlNotFoundError


def test_get_watched_url_value_error():
    """Tests if non int raises ValueError"""
    with pytest.raises(ValueError):
        persistance.get_watched_url("a")


def test_get_watched_url_Watched_Url_Not_Found_Error():
    """Tests if invalid url raises WatchedUrlNotFoundError"""
    with pytest.raises(WatchedUrlNotFoundError):
        persistance.get_watched_url(1)
