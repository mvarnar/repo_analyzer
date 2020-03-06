import argparse

from stats import (extract_commit_stats,
                   extract_pulls_stats,
                   extract_old_pulls_stats,
                   extract_issues_stats,
                   extract_old_issues_stats)
from github_api import GithubApiWrapper

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('repo_url', help='Url of github repository to analyze')
parser.add_argument('--branch', help='Branch to analyze (master by default)', default='master')
args = parser.parse_args()


def parse_url(url):
    return url.split('/')[-2:]


owner, repo = parse_url(args.repo_url)
branch = args.branch
top_n = 30
from_datetime = None
to_datetime = None
stats = []
print(owner, repo, branch, top_n, from_datetime, to_datetime)
api_wrapper = GithubApiWrapper(owner, repo)
api_commits = api_wrapper.get_commits(branch)
stats.append(extract_commit_stats(api_commits, top_n, from_datetime, to_datetime))

api_pulls = api_wrapper.get_pulls(branch, 'all')
stats.append(extract_pulls_stats(api_pulls, from_datetime, to_datetime))
stats.append(extract_old_pulls_stats(api_pulls, from_datetime, to_datetime))

api_issues = api_wrapper.get_issues('all')
stats.append(extract_issues_stats(api_issues, from_datetime, to_datetime))
stats.append(extract_old_issues_stats(api_pulls, from_datetime, to_datetime, 0))

for stat in stats:
    print(stat)
    print('------------------------------')
