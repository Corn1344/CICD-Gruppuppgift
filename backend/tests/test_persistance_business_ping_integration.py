"""Testing the integration between persistance.py and business.py"""
from datetime import datetime
from datetime import timezone
from pingurl import business
from pingurl import persistance
from pingurl import ping
from pingurl.models import WatchedUrl


# @pytest.fixture(scope="function", autouse=True)
# def reset_persistance():
#     """Resets global variables between tests"""
#     pings_before = persistance.pings
#     watched_urls_before = persistance.watched_urls
#     next_id_before = persistance.next_id
#     yield
#     persistance.pings = pings_before
#     persistance.watched_urls = watched_urls_before
#     persistance.next_id = next_id_before


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
