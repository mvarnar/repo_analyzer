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
    raw_stats = _extract_commit_raw_stats(commits, top_n, from_datetime, to_datetime)
    return _build_table(f'Top {top_n} commiters',
                        raw_stats,
                        {'commit|author|name': 'Author', 'len': 'Number of commits'})


def extract_pulls_stats(pulls, from_datetime, to_datetime):
    raw_stats = _extract_state_like_objects_stats(pulls, from_datetime, to_datetime)
    return _build_table('Pull requests', raw_stats, {'state': 'State', 'len': 'Number of requests'})


def extract_old_pulls_stats(pulls, from_datetime, to_datetime, old_border_days=30):
    raw_stats = _extract_state_like_old_objects_stats(pulls,
                                                      from_datetime,
                                                      to_datetime,
                                                      old_border_days)
    return _build_table('Old pull requests', raw_stats, {'len': 'Number of old requests'})


def extract_issues_stats(issues, from_datetime, to_datetime):
    raw_stats = _extract_state_like_objects_stats(issues, from_datetime, to_datetime)
    return _build_table('Issues', raw_stats, {'state': 'State', 'len': 'Number of issues'})


def extract_old_issues_stats(issues, from_datetime, to_datetime, old_border_days=14):
    raw_stats = _extract_state_like_old_objects_stats(issues,
                                                      from_datetime,
                                                      to_datetime,
                                                      old_border_days)
    return _build_table('Old issues', raw_stats, {'len': 'Number of old issues'})


def _extract_state_like_objects_stats(objects, from_datetime, to_datetime):
    pipe = pql.Pipeline([
        pql.Filter('created_at', in_range_datetime(from_datetime, to_datetime)),
        pql.GroupBy('state', len, {'open': 0, 'closed': 0}),
    ])
    return pipe.execute(objects)


def _extract_state_like_old_objects_stats(objects, from_datetime, to_datetime, old_border_days):
    old_border = datetime.utcnow() - timedelta(days=old_border_days)
    pipe = pql.Pipeline([
            pql.Filter('created_at', in_range_datetime(from_datetime, to_datetime)),
            pql.Filter('state', lambda state: state == 'open'),
            pql.Filter('created_at', in_range_datetime(None, old_border)),
            pql.GroupBy(None, len, {'all': 0}),
        ])
    return pipe.execute(objects)


def _extract_commit_raw_stats(commits, top_n, from_datetime, to_datetime):
    pipe = pql.Pipeline([
        pql.Filter('commit->author->date', in_range_datetime(from_datetime, to_datetime)),
        pql.GroupBy('commit->author->name', len),
        pql.OrderBy('len', reverse=True),
        pql.Limit(top_n)
    ])
    return pipe.execute(commits)


def _build_table(table_name, rows, field_name_mapper):
    table = table_name + '\n'
    requried_fields = field_name_mapper.keys()
    collumn_names = [field_name_mapper[row]
                     for row in rows[0].keys()
                     if row in requried_fields]
    table += '\t'.join(collumn_names) + '\n'
    for row in rows:
        filtered_row_values = [str(val) for key, val in row.items() if key in requried_fields]
        table += '\t'.join(filtered_row_values) + '\n'
    return table
