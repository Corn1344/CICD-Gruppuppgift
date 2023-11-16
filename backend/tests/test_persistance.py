"""Tests for persistance.py"""
from datetime import datetime
import pytest
from pingurl import persistance
from pingurl.models import WatchedUrl


def test_add_watched_url_str_arg_value_error():
    """Faulty type should result in ValueError"""
    with pytest.raises(ValueError):
        persistance.add_watched_url("Hello, Error")


def test_add_watched_url_has_id_value_error():
    """Faulty type should result in ValueError"""
    wu = WatchedUrl(datetime.now(), False, 1, "http://www.example.org", 0)
    with pytest.raises(ValueError):
        persistance.add_watched_url(wu)
