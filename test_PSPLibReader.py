from operator import attrgetter
import os
from unittest import TestCase
import MultiModeClasses
from PSPLIBReader import PSPLibReader

__author__ = 'bartek'

FILENAME = 'testFiles/c154_3.mm'


class TestPSPLibReader(TestCase):
    def test_read(self):
        psplib_reader = PSPLibReader()
        problem = psplib_reader.read(os.path.realpath(FILENAME))
        self.assertIsInstance(problem, MultiModeClasses.Problem)
        self.assertEqual(set([act.name for act in problem.activities_set]), set(str(i) for i in range(18)))
        modelist = [len(act.mode_list) for act in sorted(problem.non_dummy_activities())]
        self.assertEqual(modelist, 16*[3])




