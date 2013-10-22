import os
from unittest import TestCase
import MultiModeClasses
from PSPLIBReader import PSPLibReader

__author__ = 'bartek'

FILENAME = 'testFiles/c154_3.mm'


class TestPSPLibReader(TestCase):
    def test_read(self):
        jsonReader = PSPLibReader()
        problem = jsonReader.read(os.path.realpath(FILENAME))
        self.assertIsInstance(problem, MultiModeClasses.Problem)
        self.assertEqual(set([act.name for act in problem.activities_set]), set(str(i) for i in range(18)))
        modelist = [len(act.mode_list) for act in sorted(problem.non_dummy_activities(), key=attrgetter('name'))]
        self.assertEqual(modelist, [1] + 16*[3] + [1])




