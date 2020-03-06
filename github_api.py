import urllib.request
import json

GITHUB_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class GithubApiWrapper:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.api_uri = f'https://api.github.com/repos/{owner}/{repo}/'

    def get_commits(self, sha):
        url = f'{self.api_uri}commits?sha={sha}'
        return self._get(url)

    def get_pulls(self, base, state='open'):
        url = f'{self.api_uri}pulls?base={base}&state={state}'
        return self._get(url)

    def get_issues(self, state='open'):
        url = f'{self.api_uri}issues?state={state}'
        return self._get(url)

    def _get(self, url):
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            body = response.read()
        return json.loads(body)
