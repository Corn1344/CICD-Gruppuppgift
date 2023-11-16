"""Tests for PingUrl"""
import datetime
from pingurl.models import PingData


def test_ok_status():
    """Testing a valid OK status for success"""
    date = datetime.datetime.now()
    time_sec = datetime.timedelta(weeks=40, days=84, minutes=50)
    new_obj = PingData(date, time_sec, 300)
    assert new_obj.ok_status()


def test_ok_status_false():
    """Testing a valid OK status for failure"""
    date = datetime.datetime.now()
    time_sec = datetime.timedelta(weeks=40, days=84, minutes=50)
    new_obj = PingData(date, time_sec, 404)
    assert not new_obj.ok_status()

