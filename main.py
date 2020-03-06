import argparse

from stats import (extract_commit_stats,
                   extract_pulls_stats,
                   extract_old_pulls_stats,
                   extract_issues_stats,
                   extract_old_issues_stats)
from github_api import GithubApiWrapper

TOP_N_COMMITERS = 30
N_TABLE_SEPARATOR_LEN = 30
N_TABLE_SEPARATOR = '-' * N_TABLE_SEPARATOR_LEN
DATETIME_FORMAT = 'YYYY-MM-DDTHH:MM:SSZ'

parser = argparse.ArgumentParser(description='Program to print github repository statistics')
parser.add_argument('repo_url', help='Url of github repository to analyze')
parser.add_argument('--branch', help='Branch to analyze (master by default)', default='master')
parser.add_argument('--from_datetime',
                    help=(f'Start analyze from this date Format is {DATETIME_FORMAT} '
                          '(None by default)'),
                    default=None)
parser.add_argument('--to_datetime',
                    help=(f'Analysis will stop at this date. Format is {DATETIME_FORMAT} '
                          '(None by default)'),
                    default=None)
args = parser.parse_args()


owner, repo = args.repo_url.split('/')[-2:]
branch = args.branch
from_datetime = GithubApiWrapper.convert_from_github_datetime(
    args.from_datetime) if args.from_datetime else None
to_datetime = GithubApiWrapper.convert_from_github_datetime(
    args.to_datetime) if args.to_datetime else None

stats = []

api_wrapper = GithubApiWrapper(owner, repo)
api_commits = api_wrapper.get_commits(branch)
stats.append(extract_commit_stats(api_commits, TOP_N_COMMITERS, from_datetime, to_datetime))

api_pulls = api_wrapper.get_pulls(branch, 'all')
stats.append(extract_pulls_stats(api_pulls, from_datetime, to_datetime))
stats.append(extract_old_pulls_stats(api_pulls, from_datetime, to_datetime))

api_issues = api_wrapper.get_issues('all')
stats.append(extract_issues_stats(api_issues, from_datetime, to_datetime))
stats.append(extract_old_issues_stats(api_pulls, from_datetime, to_datetime, 0))

for stat in stats:
    print(stat)
    print(N_TABLE_SEPARATOR)
