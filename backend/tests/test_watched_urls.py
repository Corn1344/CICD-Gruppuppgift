"""Tests for pingurl/watched_urls.py"""
from datetime import datetime, timezone
import pytest
from pingurl import models, business, watched_urls
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
    url = "http://www.example.org"
    dt1 = datetime(2023, 1, 1, tzinfo=timezone.utc)
    new_url = models.WatchedUrl(dt1, True, 1, url)
    business.add_watched_url(new_url)
    with app.app_context():
        response = flask_test.get("/watched-urls/1")
    assert response.status_code == 200



def test_post_watched_urls_err_wrong_time_format(flask_test):
    """mock test bad request from wrong time format"""
    resp_data = b"The 'activateAt' parameter must an ISO 8601 date-time.\"}"

    url = "http://www.example.com"
    dt1 = datetime(2023, 1, 1, tzinfo=timezone.utc)

    json_input = {"activateAt": dt1, "force": True, "periodSec": 30, "url": url}

    response = flask_test.post("/watched-urls", json=json_input)
    assert response.status_code == 400
    assert resp_data in response.data

def test_post_watched_urls(flask_test):
    """This is a mock test that send a post request to /watched-urls,
    and then a get request to /watched_urls/<id> from the id it got
    to see that the url object was created."""
    json_query = {
        "activateAt": "2023-11-06T01:36:28+00:00",
        "force": True,
        "periodSec": 30,
        "url": "http://dn.se"
        }
    response = flask_test.post('/watched-urls', json=json_query)
    urlId = response.json["urlId"]
    response = flask_test.get("/watched-urls/" + str(urlId))
    assert response.status_code == 200
