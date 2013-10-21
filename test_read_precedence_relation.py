from unittest import TestCase
from PSPLIBReader import read_precedence_relation

__author__ = 'Aleksandra'


class TestRead_precedence_relation(TestCase):
    def test_read_precedence_relation(self):


        l1 = ['1        1          3           2   3   4',
              ' 2        3          2           5  10',
             ]

        result_dict = {'1':['2','3','4'],'2':['5','10']}
        self.assertEqual(read_precedence_relation(l1), result_dict)
