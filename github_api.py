import urllib.request
import json
from typing import List, Dict, Any


class GithubApiWrapper:
    def __init__(self, owner: str, repo: str):
        self.owner = owner,
        self.repo = repo
        self.api_uri = f'https://api.github.com/repos/{owner}/{repo}/'

    def get_commits(self, sha: str) -> List[Dict[Any, Any]]:
        url = f'{self.api_uri}commits?sha={sha}'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            body = response.read()
        return json.loads(body)
