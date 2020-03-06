from unittest import TestCase

from parameterized import parameterized, parameterized_class

from . import pql


@parameterized_class(['objects'],
                     [
                         [[pql.PQLDict({'author': {'first name': 'max', 'stat': 1}}),
                           pql.PQLDict({'author': {'first name': 'max', 'stat': 3}}),
                           pql.PQLDict({'author': {'first name': 'vasya', 'stat': -1}}),
                           pql.PQLDict({'author': {'first name': 'vasya', 'stat': 3}}),
                           pql.PQLDict({'author': {'first name': 'vasya', 'stat': 4}}), ]]
                      ])
class TestPQL(TestCase):
    @parameterized.expand([
        ('author->first name',
         len,
         {'masha': 0},
         [{'author|first name': 'max', 'len': 2},
          {'author|first name': 'vasya', 'len': 3},
          {'author|first name': 'masha', 'len': 0}])
    ])
    def test_groupby(self, field, aggregation_func, default_groups, expected):
        result = pql.GroupBy(field, aggregation_func, default_groups).execute(
            self.objects)  # pylint: disable=no-member
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('author->first name',
         lambda x: x == 'max',
         [pql.PQLDict({'author': {'first name': 'max', 'stat': 1}}),
          pql.PQLDict({'author': {'first name': 'max', 'stat': 3}})])
    ])
    def test_filter(self, field, filter_func, expected):
        result = pql.Filter(field, filter_func).execute(self.objects)  # pylint: disable=no-member
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('author->stat',
         False,
         [pql.PQLDict({'author': {'first name': 'vasya', 'stat': -1}}),
          pql.PQLDict({'author': {'first name': 'max', 'stat': 1}}),
          pql.PQLDict({'author': {'first name': 'max', 'stat': 3}}),
          pql.PQLDict({'author': {'first name': 'vasya', 'stat': 3}}),
          pql.PQLDict({'author': {'first name': 'vasya', 'stat': 4}}), ]
         ),

        ('author->stat',
         True,
         [pql.PQLDict({'author': {'first name': 'vasya', 'stat': 4}}),
          pql.PQLDict({'author': {'first name': 'max', 'stat': 3}}),
          pql.PQLDict({'author': {'first name': 'vasya', 'stat': 3}}),
          pql.PQLDict({'author': {'first name': 'max', 'stat': 1}}),
          pql.PQLDict({'author': {'first name': 'vasya', 'stat': -1}}), ]
         ),
    ])
    def test_order_by(self, field, reverse, expected):
        result = pql.OrderBy(field, reverse).execute(self.objects)  # pylint: disable=no-member
        self.assertEqual(result, expected)

    @parameterized.expand([
        (3,
         [pql.PQLDict({'author': {'first name': 'max', 'stat': 1}}),
          pql.PQLDict({'author': {'first name': 'max', 'stat': 3}}),
          pql.PQLDict({'author': {'first name': 'vasya', 'stat': -1}}), ]
         )
    ])
    def test_limit(self, limit, expected):
        result = pql.Limit(limit).execute(self.objects)  # pylint: disable=no-member
        self.assertEqual(result, expected)
