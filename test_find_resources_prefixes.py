from unittest import TestCase
from PSPLIBReader import find_resources_prefixes


__author__ = 'Aleksandra'


class TestFind_resources_prefixes(TestCase):
   def test_find_resources_prefixes(self):
#  - renewable                 :  2   R
#  - nonrenewable              :  2   N
#  - doubly constrained        :  0   D

        lines = ['  - renewable                 :  2   R',
                 '  - nonrenewable              :  2   N',
                 '  - doubly constrained        :  0   D']

        result_list= ['R','N','D']
        self.assertEqual(find_resources_prefixes(lines), result_list)