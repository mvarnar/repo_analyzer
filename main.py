from stats import extract_commit_stats, extract_pr_stats, extract_issue_stats

owner = 'mvarnar'
repo = 'test'
branch = 'test_branch'
top_n = 30
stats = []


stats.append(extract_commit_stats(owner, repo, branch, top_n))
stats.append(extract_pr_stats(owner, repo))
stats.append(extract_issue_stats(owner, repo))

for stat in stats:
    print(stat)
    print('\n------------------------------\n')
