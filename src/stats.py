from datetime import datetime

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
    pipe = pql.Pipeline([
        pql.Filter('created_at', in_range_datetime(from_datetime, to_datetime)),
        pql.GroupBy('state', len),
    ])
    return pipe.execute(pulls)
