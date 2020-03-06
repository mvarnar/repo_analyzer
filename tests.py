from unittest import TestCase

from parameterized import parameterized

from stats import _build_table


class TestStats(TestCase):
    @parameterized.expand([
        ('table_name',
         [{'state': 'open', 'len': 1, 'some': 3}, {'state': 'closed', 'len': 1, 'some': 4}],
         {'state': 'State', 'len': 'Number of issues', 'other': 'Other'},
         ('table_name\n'
          'State\tNumber of issues\n'
          'open\t1\n'
          'closed\t1\n'))
    ])
    def test__build_table(self, table_name, rows, field_name_mapper, expected):
        result = _build_table(table_name, rows, field_name_mapper)
        self.assertEqual(result, expected)
