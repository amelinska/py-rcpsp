from collections import defaultdict
import json
import MultiModeClasses


__author__ = 'bartek'


class ResourceParser(object):
    RENEWABLE_RESOURCES_TAG = "renewable_resources"
    NON_RENEWABLE_RESOURCES_TAG = "non_renewable_resources"
    def __init__(self, jsonDictionary):
        self.resources = {int(i): jsonDictionary[i] for i in jsonDictionary}

    def parse(self):
        return self.resources

class ProjectParser(object):
    def parse(self):
        raise NotImplementedError()

class JSONParsingError(Exception):
    pass


class ModeParser(object):
    DURATION_TAG = "duration"
    DEMAND_TAG = "demand"
    NONRENEWABLE_DEMAND = "non_renewable_demand"
    def __init__(self, name, jsonDictionary):
        d = jsonDictionary[self.DURATION_TAG]
        demand = ResourceParser(jsonDictionary[self.DEMAND_TAG]).parse()
        if self.NONRENEWABLE_DEMAND in jsonDictionary:
            non_renewable_demand = ResourceParser(jsonDictionary[self.NONRENEWABLE_DEMAND]).parse()
            self.mode = MultiModeClasses.Mode(name, d, demand, non_renewable_demand)
        else:
            self.mode = MultiModeClasses.Mode(name, d, demand)

    def parse(self):
        return self.mode


class ActivityParser(object):
    def __init__(self, name, jsonDictionary):
        modes = []
        for k,v in jsonDictionary.iteritems():
            mode = ModeParser(k, v).parse()
            modes.append(mode)
        self.activity = MultiModeClasses.Activity(name, modes)

    def parse(self):
        return self.activity


class ActivitiesParser(object):
    ACTIVITIES_TAG = "activities"
    def __init__(self, jsonDictionary):
        self.result = {}
        for key, activityJson in jsonDictionary.iteritems():
            self.result[key] = ActivityParser(key, activityJson).parse()

    def parse(self):
        return self.result


class RelationParser(object):
    GRAPH_PRECEDENCE_TAG = "activity_graph"
    def __init__(self, jsonDictionary):
        self.jsonDictionary = jsonDictionary

    def parse(self):
        return self.jsonDictionary


class MultimodeParser(ProjectParser):
    def __init__(self, jsonDictionary):
        self.jsonDictionary = jsonDictionary

    def parse(self):
        parser = ResourceParser(self.jsonDictionary[ResourceParser.RENEWABLE_RESOURCES_TAG])
        renewable_resources = parser.parse()
        parser = ResourceParser(self.jsonDictionary[ResourceParser.NON_RENEWABLE_RESOURCES_TAG])
        non_renewable_resources = parser.parse()
        activity_dictionary = ActivitiesParser(self.jsonDictionary[ActivitiesParser.ACTIVITIES_TAG]).parse()
        relation_dictionary = RelationParser(self.jsonDictionary[RelationParser.GRAPH_PRECEDENCE_TAG]).parse()
        activity_graph = self._createGraph(activity_dictionary, relation_dictionary)
        return MultiModeClasses.Problem(activity_graph, renewable_resources, non_renewable_resources)

    def _createGraph(self, activity_dictionary, relation_dictionary):
        resulting_graph = defaultdict(list)
        for preceding_activity, list_of_next in relation_dictionary:
            try:
                for successor in list_of_next:
                    resulting_graph[activity_dictionary[preceding_activity]].append(activity_dictionary[successor])
            except KeyError:
                raise JSONParsingError("Cannot find corresponding activity in relation")
        return resulting_graph

class SinglemodeParser(ProjectParser):
    def __init__(self, jsonDictionary):
        pass

    def parse(self):
        pass


class JSONProjectReader(object):
    PROBLEM_TYPE_TAG = "problem_type"
    PROBLEM_TAG ="problem"
    MUTLIMODE_PROBLEM_TYPE = "multimode"
    SINGLE_MODE_PROBLEM_TYPE = "singlemode"


    def read(self, filename):
        """

        :param filename: absolute path to json file containing project description
        :return: Project instance described in json file
        :rtype:
        """
        with open(filename) as file:
            content = "".join(file.readlines())
            self._rawJSONContent = json.loads(content)
            parser = self.retrieveType()
            return parser.parse()

    def retrieveType(self):
        problem_type = self._rawJSONContent[self.PROBLEM_TYPE_TAG]
        if problem_type == self.MUTLIMODE_PROBLEM_TYPE:
            return MultimodeParser(self._rawJSONContent[self.PROBLEM_TAG])
        elif problem_type == self.SINGLE_MODE_PROBLEM_TYPE:
            return SinglemodeParser(self._rawJSONContent[self.PROBLEM_TAG])
        else:
            raise JSONParsingError("Cannot find parser for given type")
        #TODO: end writing JSON project reader and test it




