import urllib.request
import json
from typing import List, Dict, Any

GITHUB_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class GithubApiWrapper:
    def __init__(self, owner: str, repo: str):
        self.owner = owner,
        self.repo = repo
        self.api_uri = f'https://api.github.com/repos/{owner}/{repo}/'

    def get_commits(self, sha: str) -> List[Dict[Any, Any]]:
        url = f'{self.api_uri}commits?sha={sha}'
        return self._get(url)

    def get_pulls(self, base: str, state: str = 'open') -> List[Dict[Any, Any]]:
        url = f'{self.api_uri}pulls?base={base}&state={state}'
        return self._get(url)

    def _get(self, url: str) -> Any:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            body = response.read()
        return json.loads(body)
