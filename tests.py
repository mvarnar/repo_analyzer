# type: ignore
from unittest import TestCase
from datetime import datetime

from parameterized import parameterized

from stats import (Commit,
                   _build_commits_from_api_commits,
                   _get_top_n_authors,
                   _build_top_n_authors_table)


class TestCommitStatsExtraction(TestCase):
    @parameterized.expand([
        ([{'commit': {'author': {'name': 'someone', 'date': '2020-03-03T16:35:57Z'}}},
          {'commit': {'author': {'name': 'someother', 'date': '2020-03-04T00:00:57Z'}}}],
         [Commit(author='someone', timestamp=datetime(2020, 3, 3, 16, 35, 57)),
          Commit(author='someother', timestamp=datetime(2020, 3, 4, 0, 0, 57))])
    ])
    def test__build_commits_from_api_commits(self, api_commits, expected):
        result = _build_commits_from_api_commits(api_commits)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ([Commit(author='1', timestamp=datetime(2020, 1, 1)),
          Commit(author='1', timestamp=datetime(2020, 1, 2)),
          Commit(author='2', timestamp=datetime(2018, 1, 1)),
          Commit(author='2', timestamp=datetime(2019, 12, 31)),
          Commit(author='2', timestamp=datetime(2019, 12, 30)),
          Commit(author='3', timestamp=datetime(2018, 1, 1))],
         2,
         datetime(2019, 12, 30),
         datetime(2020, 1, 1),
         [('2', 2), ('1', 1)]),

        ([Commit(author='1', timestamp=datetime(2020, 1, 1)),
          Commit(author='1', timestamp=datetime(2020, 1, 2)),
          Commit(author='2', timestamp=datetime(2018, 1, 1)),
          Commit(author='2', timestamp=datetime(2019, 12, 31)),
          Commit(author='2', timestamp=datetime(2019, 12, 30)),
          Commit(author='3', timestamp=datetime(2018, 1, 1))],
         3,
         None,
         None,
         [('2', 3), ('1', 2), ('3', 1)]),

        ([Commit(author='1', timestamp=datetime(2020, 1, 1)),
            Commit(author='1', timestamp=datetime(2020, 1, 2)),
            Commit(author='2', timestamp=datetime(2018, 1, 1)),
            Commit(author='2', timestamp=datetime(2019, 12, 31)),
            Commit(author='2', timestamp=datetime(2019, 12, 30)),
            Commit(author='3', timestamp=datetime(2018, 1, 1))],
         2,
         None,
         None,
         [('2', 3), ('1', 2)])
    ])
    def test__get_top_n_authors(self, commits, n, from_date, to_date, expected):
        author_stats = _get_top_n_authors(commits, n, from_date, to_date)
        self.assertEqual(author_stats, expected)

    @parameterized.expand([
        ([('2', 2), ('1', 1)], ('Author\tNumber of commits\n'
                                '2\t2\n'
                                '1\t1\n')),
    ])
    def test__build_top_n_authors_table(self, author_stats, expected):
        table = _build_top_n_authors_table(author_stats)
        self.assertEqual(table, expected)
