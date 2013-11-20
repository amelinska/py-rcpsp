from unittest import TestCase
#from pyrcpsp.PSPLIBReader import find_resources_prefixes
from pyrcpsp import  PSPLIBReader

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
        self.assertEqual(PSPLIBReader.find_resources_prefixes(lines), result_list)