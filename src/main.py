from stats import extract_commit_stats, extract_pulls_stats
from github_api import GithubApiWrapper

owner = 'mvarnar'
repo = 'test'
branch = 'master'
top_n = 30
from_datetime = None
to_datetime = None
stats = []

api_wrapper = GithubApiWrapper(owner, repo)
api_commits = api_wrapper.get_commits(branch)
stats.append(extract_commit_stats(api_commits, top_n, from_datetime, to_datetime))

api_pulls = api_wrapper.get_pulls(branch, 'all')
stats.append(extract_pulls_stats(api_pulls, from_datetime, to_datetime))

# stats.append(extract_issue_stats(owner, repo))

for stat in stats:
    print(stat)
    print('\n------------------------------\n')
