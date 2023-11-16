"""Tests for PingUrl"""
from datetime import datetime, timezone, timedelta
from pingurl.models import PingData, WatchedUrl
import pingurl.persistance
import pingurl.business


def test_PingData_ok_status():
    """Testing a valid OK status for success in class PingData"""
    date = datetime.now()
    time_sec = timedelta(weeks=40, days=84, minutes=50)
    new_obj = PingData(date, time_sec, 300)
    assert new_obj.ok_status()


def test_PingData_ok_status_false():
    """Testing a valid OK status for failure in class PingData"""
    date = datetime.now()
    time_sec = timedelta(weeks=40, days=84, minutes=50)
    new_obj = PingData(date, time_sec, 404)
    assert not new_obj.ok_status()


def test_to_dict():
    """Testing... in class WatchedUrl"""
    watchedUrls = []
    urls = []
    url = "http://www.example.org"
    dt1 = datetime(2023, 1, 1, tzinfo=timezone.utc)
    new_url = WatchedUrl(dt1, True, 1, url)
    url_id = pingurl.business.add_watched_url(new_url)
    url1 = WatchedUrl(dt1, True, 1, url)
    url2 = WatchedUrl(dt1, False, 2, url)
    watchedUrls.append(url1)
    watchedUrls.append(url2)
    for url in watchedUrls:
        urls.append(pingurl.persistance.add_watched_url(url))
    print (urls)
    assert url_id in pingurl.persistance.get_url_ids()
    assert len(urls) == 2
