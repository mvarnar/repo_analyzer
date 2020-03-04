import urllib.request
import json
from dataclasses import dataclass
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple


@dataclass
class Commit:
    author: str
    timestamp: datetime


@dataclass
class PR:
    pass


@dataclass
class Issue:
    pass


def extract_commit_stats(owner: str,
                         repo: str,
                         branch: str,
                         top_n: int,
                         from_datetime: Optional[datetime] = None,
                         to_datetime: Optional[datetime] = None) -> str:
    api_commits = _get_commits_from_api(owner, repo, branch)
    commits = _build_commits_from_api_commits(api_commits)
    top_n_authors = _get_top_n_authors(commits, top_n, from_datetime, to_datetime)
    return _build_top_n_authors_table(top_n_authors)


def extract_pr_stats(owner: str, repo: str) -> str:
    pass


def extract_issue_stats(owner: str, repo: str) -> str:
    pass


def _get_commits_from_api(owner: str, repo: str, branch: str) -> List[Dict[Any, Any]]:
    url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        body = response.read()
    return json.loads(body)


def _build_commits_from_api_commits(api_commits: List[Dict[Any, Any]]) -> List[Commit]:
    commits = []
    for api_commit in api_commits:
        author = api_commit['commit']['author']['name']
        timestamp = datetime.strptime(api_commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        commits.append(Commit(author=author, timestamp=timestamp))
    return commits


def _get_top_n_authors(commits: List[Commit],
                       n: int,
                       from_datetime: Optional[datetime] = None,
                       to_datetime: Optional[datetime] = None) -> List[Tuple[str, int]]:
    author_counter: Dict[str, int] = Counter()
    for commit in commits:
        if ((from_datetime is None or from_datetime <= commit.timestamp)
            and (to_datetime is None or commit.timestamp <= to_datetime)):
            author_counter[commit.author] += 1
    author_stats = sorted(author_counter.items(), key=lambda x: x[1], reverse=True)
    return author_stats[:n]


def _build_top_n_authors_table(autor_stats: List[Tuple[str, int]]) -> str:
    table = 'Author\tNumber of commits\n'
    for author_score in autor_stats:
        table += f'{author_score[0]}\t{author_score[1]}\n'
    return table
