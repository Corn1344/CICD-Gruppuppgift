"""Tests for pingurl/watched_urls.py"""
from datetime import datetime, timezone
import pytest
from pingurl import models, business, watched_urls, persistance, schedule
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
    url_id = business.add_watched_url(new_url)
    with app.app_context():
        response = flask_test.get(f"/watched-urls/{url_id}")
    assert response.status_code == 200


def test_deletr_url_err(flask_test):
    """This is a mock test that send a delete request to /watched-urls/0,
    should return error status_code = 404"""
    response = flask_test.delete("/watched-urls/0")
    assert response.status_code == 404


def test_delete_url(flask_test):
    """Test if url can be deleted."""
    schedule.jobs = {}
    url = "http://www.example.org"
    dt1 = datetime(2023, 1, 1, tzinfo=timezone.utc)
    new_url = models.WatchedUrl(dt1, True, 1, url)
    url_id = business.add_watched_url(new_url)
    response = flask_test.delete(f"/watched-urls/{url_id}")
    print(response)
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
        "url": "http://dn.se",
    }
    response = flask_test.post("/watched-urls", json=json_query)
    url_id = response.json["urlId"]
    response = flask_test.get("/watched-urls/" + str(url_id))
    assert response.status_code == 200


def test_no_wurl_get_stats():
    """This is a mock test that doesn't add any url to the watched list
    and makes sure it does not return any stats"""
    response = persistance.get_stats()
    assert response == {"watchedUrls": 0, "pings": 0}


def test_get_stats():
    """In this test we add an URL to the watched list and use get stats and make sure there
    is an added URL and that it gets pinged when added"""
    url = "http://www.example.org"
    dt1 = datetime(2023, 1, 1, tzinfo=timezone.utc)
    new_url = models.WatchedUrl(dt1, True, 1, url)
    business.add_watched_url(new_url)
    response = persistance.get_stats()
    assert response == {"watchedUrls": 1, "pings": 2}
