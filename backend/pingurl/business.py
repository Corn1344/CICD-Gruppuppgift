"""business"""
from pingurl import schedule, persistance
from pingurl.models import WatchedUrl
from pingurl.ping import send_ping


def add_watched_url(watched_url):
    """adds watched url"""
    if not isinstance(watched_url, WatchedUrl):
        raise ValueError("watched_url must be a WatchedUrl instance")

    ping_data = send_ping(watched_url)

    if not ping_data.ok_status() and not watched_url.force:
        raise AddWatchedUrlError("Ping failed and force is false")

    url_id = persistance.add_watched_url(watched_url)

    # Add the created url_id to the ping_data object
    ping_data.url_id = url_id

    persistance.add_ping_data(ping_data)

    schedule.add_url(watched_url)

    return url_id


def delete_watched_url(url_id):
    """deletes watched url"""
    if not isinstance(url_id, int):
        raise ValueError("url_id must be an integer")

    schedule.remove_url(url_id)

    persistance.delete_watched_url(url_id)


class AddWatchedUrlError(Exception):
    """raise watched url error"""
