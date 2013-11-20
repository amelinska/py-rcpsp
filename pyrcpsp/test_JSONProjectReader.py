import json
from operator import attrgetter
from unittest import TestCase
import os

import JsonProjectReader
from pyrcpsp import MultiModeClasses


__author__ = 'bartek'

FILENAME = 'testFiles/sampleProject.json'


class TestJSONProjectReader(TestCase):
    def test_read(self):
        jsonReader = JsonProjectReader.JSONProjectReader()
        problem = jsonReader.read(os.path.realpath(FILENAME))
        self.assertIsInstance(problem, MultiModeClasses.Problem)
        self.assertEqual(set([act.name for act in problem.non_dummy_activities()]), set(str(i) for i in range(1,7)))
        modelist = [len(act.mode_list) for act in sorted(problem.activities(), key=attrgetter('name'))]
        self.assertEqual(modelist, [2, 2, 2, 2, 2, 2, 1, 1])

        modelist = [len(act.mode_list) for act in sorted(problem.non_dummy_activities(), key=attrgetter('name'))]
        self.assertEqual(modelist, [2, 2, 2, 2, 2, 2])


class TestResourceParser(TestCase):
    def test_parse(self):
        jsonDictionary = json.loads("{\"1\": 4}")
        p = JsonProjectReader.ResourceParser(jsonDictionary)
        self.assertEqual(p.parse(), {1: 4})

class TestDummyNodesParser(TestCase):
    def test_parse(self):
        jsonDictionary = json.loads("{\"dummy_start\": \"0\",\"dummy_end\": \"7\"}")
        p = JsonProjectReader.DummyNodesParser(jsonDictionary)
        self.assertEqual(p.parse(), ("0","7"))


class TestActivitiesParser(TestCase):
    def test_parse(self):
        activities = """
        {
            "d" : {},
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
        p = JsonProjectReader.ActivitiesParser(jsonDictionary, dummy_start="d", dummy_end="2")
        activity_dictionary = p.parse()
        self.assertEqual(len(activity_dictionary), 3)
        for k, v in activity_dictionary.iteritems():
            self.assertIsInstance(v, MultiModeClasses.Activity)
            if not k == "d":
                self.assertEqual(k, v.name)
        dummy_start = activity_dictionary["d"]
        self.assertEqual(dummy_start, MultiModeClasses.Activity.DUMMY_START)


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
        p = JsonProjectReader.ActivityParser("somename", jsonDictionary, dummy_start="0", dummy_end="1")
        a = p.parse()
        self.assertIsInstance(a, MultiModeClasses.Activity)
        self.assertEqual(a.maximal_duration(), 4)
        self.assertEqual(a.minimal_duration(), 3)
        self.assertEqual(len(a.mode_list), 2)
        self.assertEqual(a.name, "somename")

    def test_parse_dummy(self):
        activity_string = "{}"
        jsonDictionary = json.loads(activity_string)
        p = JsonProjectReader.ActivityParser("0", jsonDictionary, dummy_start="0", dummy_end="1")
        a = p.parse()
        self.assertIsInstance(a, MultiModeClasses.Activity)
        self.assertEqual(a, MultiModeClasses.Activity.DUMMY_START)
        self.assertEqual(a.name, "start")


class TestModeParser(TestCase):
    def test_parse(self):
        mode_string = """
        {
            "duration" : 4,
            "demand" : {"1": 1, "2": 1}
        }
        """
        jsonDictionary = json.loads(mode_string)
        p = JsonProjectReader.ModeParser("somename", jsonDictionary)
        mode = p.parse()
        self.assertIsInstance(mode, MultiModeClasses.Mode)
        self.assertEqual(mode.demand, {1: 1, 2: 1})
        self.assertEqual(mode.duration, 4)
