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
    wu = WatchedUrl(dt, False, 1, "http://www.example.org")
    wu.url_id = business.add_watched_url(wu)
    pd = ping.send_ping(wu)
    urls = persistance.get_url_ids()
    assert wu.url_id in urls
    assert pd.url_id in urls
