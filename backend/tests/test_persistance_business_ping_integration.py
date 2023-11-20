"""Testing the integration between persistance.py and business.py"""
from datetime import datetime
from datetime import timezone
from pingurl import business
from pingurl import persistance
from pingurl import ping
from pingurl.models import WatchedUrl


def test_added_url_in_get_urls():
    """
    Tests if persistance.get_url_ids() can get
    urls added from business.add_watched_url
    """
    dt = datetime(2023, 11, 16, tzinfo=timezone.utc)
    wu = WatchedUrl(dt, True, 1, "http://www.example.org")
    wu.url_id = business.add_watched_url(wu)
    pd = ping.send_ping(wu)
    urls = persistance.get_url_ids()
    assert wu.url_id in urls
    assert pd.url_id in urls


def test_added_url_and_ping_in_get_stats():
    """
    Tests if persistance.get_stats() can receive
    no. of urls and pings added from business.add_watched_url()
    and ping.send_ping()
    """

    dt = datetime(2023, 11, 16, tzinfo=timezone.utc)
    wu_list = [
        WatchedUrl(dt, True, 1, "http://www.example.org"),
        WatchedUrl(dt, True, 1, "http://www.example.org"),
    ]
    for wu in wu_list:
        business.add_watched_url(wu)
        pd = ping.send_ping(wu)
        persistance.add_ping_data(pd)
    stats = persistance.get_stats()
    assert stats == {"watchedUrls": 2, "pings": 4}
