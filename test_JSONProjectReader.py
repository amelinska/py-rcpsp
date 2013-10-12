import json
from operator import attrgetter
from unittest import TestCase
from JsonProjectReader import JSONProjectReader, ResourceParser, ActivitiesParser, ActivityParser, ModeParser
import os
import MultiModeClasses

__author__ = 'bartek'

FILENAME = 'testFiles/sampleProject.json'


class TestJSONProjectReader(TestCase):
    def test_read(self):
        jsonReader = JSONProjectReader()
        problem = jsonReader.read(os.path.realpath(FILENAME))
        self.assertIsInstance(problem, MultiModeClasses.Problem)
        self.assertEqual(set([act.name for act in problem.activities_set]), set(str(i) for i in range(8)))
        modelist = [len(act.mode_list) for act in sorted(problem.non_dummy_activities(), key=attrgetter('name'))]
        self.assertEqual(modelist, [1, 2, 2, 2, 2, 2, 2, 1])


class TestResourceParser(TestCase):
    def test_parse(self):
        jsonDictionary = json.loads("{\"1\": 4}")
        p = ResourceParser(jsonDictionary)
        self.assertEqual(p.parse(), {1: 4})


class TestActivitiesParser(TestCase):
    def test_parse(self):
        activities = """
        {
            "0" : {
                "mode1" : {
                    "duration" : 0,
                    "demand" : {"1": 0,"2": 0}
                }
            },
            "1" : {
                "mode1" : {
                    "duration" : 3,
                    "demand" : {"1": 2, "2": 5}
                },
                "mode2" : {
                    "duration" : 4,
                    "demand" : {"1": 1, "2": 1}
                }
            }
        }
        """
        jsonDictionary = json.loads(activities)
        p = ActivitiesParser(jsonDictionary)
        activity_dictionary = p.parse()
        self.assertEqual(len(activity_dictionary), 2)
        for k, v in activity_dictionary.iteritems():
            self.assertIsInstance(v, MultiModeClasses.Activity)
            self.assertEqual(k, v.name)


class TestActivityParser(TestCase):
    def test_parse(self):
        activity_string = """
            {
                "mode1" : {
                    "duration" : 3,
                    "demand" : {"1": 2, "2": 5}
                },
                "mode2" : {
                    "duration" : 4,
                    "demand" : {"1": 1, "2": 1}
                }
            }
            """
        jsonDictionary = json.loads(activity_string)
        p = ActivityParser("somename", jsonDictionary)
        a = p.parse()
        self.assertIsInstance(a, MultiModeClasses.Activity)
        self.assertEqual(a.maximal_duration(), 4)
        self.assertEqual(a.minimal_duration(), 3)
        self.assertEqual(len(a.mode_list), 2)
        self.assertEqual(a.name, "somename")


class TestModeParser(TestCase):
    def test_parse(self):
        mode_string = """
        {
            "duration" : 4,
            "demand" : {"1": 1, "2": 1}
        }
        """
        jsonDictionary = json.loads(mode_string)
        p = ModeParser("somename", jsonDictionary)
        mode = p.parse()
        self.assertIsInstance(mode, MultiModeClasses.Mode)
        self.assertEqual(mode.demand, {1: 1, 2: 1})
        self.assertEqual(mode.duration, 4)
