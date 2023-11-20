"""Tests for pingurl/watched_urls.py"""
from datetime import datetime, timezone
import pytest
from pingurl import models, business, watched_urls, persistance
from app import app


obj = watched_urls


@pytest.fixture(scope="function", name="flask_test")
def flask_test_client():
    """This is for mocktest of flask application"""
    with app.test_client() as client:
        yield client


def test_get_watched_urls_err(flask_test):
    """This is a mock test that send a get request to /watched-urls/0,
    should return error status_code = 404"""
    response = flask_test.get("/watched-urls/0")
    assert response.status_code == 404


def test_get_watched_urls(flask_test):
    """This is a mock test that sends a get request to /watched-urls/1,
    since i added an url with id 1 it should return
    status code 200"""
    persistance.next_id = 1

    url = "http://www.example.org"
    dt1 = datetime(2023, 1, 1, tzinfo=timezone.utc)
    new_url = models.WatchedUrl(dt1, True, 1, url)
    business.add_watched_url(new_url)
    with app.app_context():
        response = flask_test.get("/watched-urls/1")
    assert response.status_code == 200
