from datetime import datetime, timedelta

from pql import pql
from github_api import GITHUB_DATETIME_FORMAT


def in_range_datetime(from_datetime=None, to_datetime=None):
    def _in_range_datetime(timestamp):
        timestamp = datetime.strptime(timestamp, GITHUB_DATETIME_FORMAT)
        return ((from_datetime is None or from_datetime <= timestamp)
                and (to_datetime is None or timestamp <= to_datetime))
    return _in_range_datetime


def extract_commit_stats(commits, top_n, from_datetime, to_datetime):
    pipe = pql.Pipeline([
        pql.Filter('commit->author->date', in_range_datetime(from_datetime, to_datetime)),
        pql.GroupBy('commit->author->name', len),
        pql.OrderBy('len', reverse=True),
        pql.Limit(top_n)
    ])
    return pipe.execute(commits)


def extract_pulls_stats(pulls, from_datetime, to_datetime):
    return _extract_state_like_objects_stats(pulls, from_datetime, to_datetime)


def extract_old_pulls_stats(pulls, from_datetime, to_datetime, old_border_days=30):
    return _extract_state_like_old_objects_stats(pulls,
                                                 from_datetime,
                                                 to_datetime,
                                                 old_border_days)


def extract_issues_stats(issues, from_datetime, to_datetime):
    return _extract_state_like_objects_stats(issues, from_datetime, to_datetime)


def extract_old_issues_stats(issues, from_datetime, to_datetime, old_border_days=14):
    return _extract_state_like_old_objects_stats(issues,
                                                 from_datetime,
                                                 to_datetime,
                                                 old_border_days)


def _extract_state_like_objects_stats(objects, from_datetime, to_datetime):
    pipe = pql.Pipeline([
        pql.Filter('created_at', in_range_datetime(from_datetime, to_datetime)),
        pql.GroupBy('state', len),
    ])
    return pipe.execute(objects)


def _extract_state_like_old_objects_stats(objects, from_datetime, to_datetime, old_border_days):
    old_border = datetime.utcnow() - timedelta(days=old_border_days)
    pipe = pql.Pipeline([
            pql.Filter('created_at', in_range_datetime(from_datetime, to_datetime)),
            pql.Filter('state', lambda state: state == 'open'),
            pql.Filter('created_at', in_range_datetime(None, old_border)),
            pql.GroupBy(None, len),
        ])
    return pipe.execute(objects)
