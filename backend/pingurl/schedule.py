"""schedule"""

from datetime import datetime, timedelta, timezone
from pingurl.ping import send_ping_persist_data
from pingurl.models import WatchedUrl
from pingurl import scheduler as apscheduler

jobs = {}

spread_start = 1


def add_url(watched_url: WatchedUrl):
    """adds url"""
    url_id = watched_url.url_id

    now = datetime.now(timezone.utc)

    if watched_url.activate_at > now:
        start_delay = watched_url.activate_at - now
    else:
        # Spread the start of the jobs by 1 second for jobs which should have
        # already been started. These jobs are most likely being added at start
        # from the database.
        global spread_start
        start_delay = timedelta(seconds=spread_start)
        spread_start += 1

    job = apscheduler.add_job(
        func=send_ping_persist_data,
        args=[url_id],  # Passing url_id as an argument to the job
        trigger="interval",
        seconds=watched_url.period_sec,
        start_date=datetime.now() + start_delay,
    )

    jobs[url_id] = job.id


def remove_url(url_id: WatchedUrl):
    """removes url"""
    job_id = jobs.get(url_id)

    if job_id is not None:
        apscheduler.remove_job(job_id)
        jobs.pop(url_id)
