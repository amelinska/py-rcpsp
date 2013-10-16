from unittest import TestCase
from GeneticAlgorithmSolverMultimode import evaluate_sgs_function
from JsonProjectReader import JSONProjectReader
from MultiModeClasses import Solution

__author__ = 'bartek'


class TestEvaluate_sgs_function(TestCase):
    def make_activities_map(self, problem):
        result = {}
        for activity in problem.activities_set:
            result[activity.name] = activity
        return result
    def setUp(self):
        self.problem = JSONProjectReader().read('testFiles/sampleProject.json')
    def test_evaluate_sgs_function(self):
        activity_map = self.make_activities_map(self.problem)
        activity_list = [activity_map[key] for key in ["2","4","1","6","3","5"]]
        mode_list = [a.get_mode_for_name(name) for a, name in zip(activity_list, ["mode2", "mode2", "mode1", "mode1", "mode1", "mode1"])]
        sgs = zip(activity_list, mode_list)
        self.assertEqual(evaluate_sgs_function(Solution, self.problem, sgs),(15,))