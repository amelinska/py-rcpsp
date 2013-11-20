import itertools
from pyrcpsp import MultiModeClasses
from pyrcpsp import ReaderInterface

class PSPLibParsingError(ReaderInterface.ReadingError):
    pass


def find_all_identifiers(result_dict):
    identifier_set = set([])
    for node, list_of_nodes in result_dict.iteritems():
        identifier_set.add(node)
        for identifier in list_of_nodes:
            identifier_set.add(identifier)
    return identifier_set

def find_start_end_tuple(result_dict):
    all_identifiers = find_all_identifiers(result_dict)
    starts = []
    ends = []
    for identifier in all_identifiers:
        potential_start = True
        potential_end = True
        for k, v in result_dict.iteritems():
            if k == identifier:
                potential_end = False
            if identifier in v:
                potential_start = False
        if potential_start:
            starts.append(identifier)
        if potential_end:
            ends.append(identifier)
    if len(starts) != 1:
        raise ValueError("There should be only one start, have {}".format(starts))
    if len(ends) != 1:
        raise ValueError("There should be only one end, have {}".format(ends))

    return starts[0], ends[0]

def read_precedence_paragraph(list_of_lines):
    mode_graph, start, end = read_precedence_relation(itertools.islice(list_of_lines, 2, None))
    return mode_graph, start, end

#TODO: test it and test it callers
def remove_element_without_successors(result_dict):
    toRemove = [k for k, v in result_dict.iteritems() if not v]
    for k in toRemove:
        del result_dict[k]

def read_precedence_relation(precedence_relation_section_lines):
    """
    :param precedence_relation_section_lines: list of strings with psplib format precedence relation description
    :type precedence_relation_section_lines: list[str]
    :return: dict defining precedence relation in the project, dict representing graph
    :rtype: dict[str] -> list[str]

    precedence_relation_section_lines:
    ['1        1          3           2   3   4',
    '2        3          2           5  10']
    return:
    {'1': ['2','3','4'], '2': ['5', '10']}
    """
    result_dict ={}
    for line in precedence_relation_section_lines:
        filtered_tokens = tokenize(line)
        result_dict[filtered_tokens[0]]=filtered_tokens[3:]
    remove_element_without_successors(result_dict)
    start_end_tuple = find_start_end_tuple(result_dict)
    return (result_dict, start_end_tuple[0], start_end_tuple[1])


def tokenize(label_line):
    label_tokens = label_line.split(' ')
    filtered_tokens = [token.strip() for token in label_tokens if len(token.strip()) > 0]
    return filtered_tokens

def group_identifiers_and_numbers(filtered_tokens):
    labels = []
    for i in range(0, len(filtered_tokens), 2):
        labels.append(filtered_tokens[i] + filtered_tokens[i + 1])
    return labels

def read_resources(label_line, capacity_line):
    """
    :param label_line: line containing labels of resources
    :type label_line: basestring
    :param capacity_line: line containing capacity of each resource
    :type capacity_line: basestring
    :return: dictionary mapping resource name to capacity of that resource

    label_line:
    'R 1  R 2  N 1  N 2'
    capacity_line:
    '20   26   23   36'
    return:
    {'R1': 20, 'R2': 26, 'N1': 23, 'N2': 36}
    """
    filtered_tokens = tokenize(label_line)
    labels = group_identifiers_and_numbers(filtered_tokens)

    capacity_tokens = tokenize(capacity_line)
    return {labels[i] : int(capacity_tokens[i]) for i in range(len(labels))}

def split_dictionary(input_dict, list_of_prefixes):
    """
    :param input_dict: dictionary to be splitted into list of dictionaries ; {"some1": 4, "some5": 2, "other5": 9}
    :param list_of_prefixes: prefixes according to which input_dict will be splitted ; ["some","other"]
    :return: list of splitted dictionaries with the same order as list_of_prefixes ; [{"some1": 4, "some5": 2}, {"other5": 9}]
    :type input_dict: dict[str]
    """
    result_list = []
    for prefix in list_of_prefixes:
        dict_for_prefix = {}
        for key in input_dict:
            if key.startswith(prefix):
                dict_for_prefix[key] = input_dict[key]
        result_list.append(dict_for_prefix)
    return result_list

def read_resources_names_paragraph(list_of_lines):
    return find_resources_prefixes(
        itertools.islice(itertools.dropwhile(lambda x : "RESOURCES" in x, list_of_lines), 1, None)
    )

#TODO: high coupling between this function and
def find_resources_prefixes(list_of_lines_with_prefixes):
    #input:
    #       ["  - renewable                 :  2   R",
    #        "  - nonrenewable              :  2   N",
    #        "  - doubly constrained        :  0   D"
    #        ]
    #
    #output:
    # {"R", "N", "D"}

    result_list = []
    for line in list_of_lines_with_prefixes:
        filtered_tokens = tokenize(line)
        resource_prefix = filtered_tokens[len(filtered_tokens)-1]
        result_list.append(str(resource_prefix))
    return result_list

def parse_modes_paragraph_header(input_line):
    tokens = tokenize(input_line)
    if tokens[0] == 'jobnr.' and tokens[1] == 'mode' and tokens[2] == 'duration':
        return group_identifiers_and_numbers(tokens[3:])
    else:
        raise PSPLibParsingError()

def find_modes_lines_generic(list_of_lines, fun):
    number_of_tokens = len(tokenize(list_of_lines[0]))
    job_dict = {}
    mode_dict = {}
    for line in list_of_lines:
        current_line = tokenize(line)
        if number_of_tokens == len(current_line):
            #definition of new job (activity) starts
            if mode_dict == {}:
                job_number = current_line[0]
            else:
                job_dict[job_number] = mode_dict
                mode_dict = {}
                job_number = current_line[0]
            mode_number = current_line[1]
            mode_dict[mode_number] = fun(current_line, 2)
        elif number_of_tokens - 1 == len(current_line):
            #it is line containing only mode (not a definition of new activity)
            mode_number = current_line[0]
            mode_dict[mode_number] = fun(current_line, 1)
        else:
            #no other types of lines are expected
            raise PSPLibParsingError("line is to short")

    job_dict[job_number] = mode_dict
    return job_dict

def find_modes_duration(list_of_lines):
    #list_of_lines:
    #["1      1     0       0    0    0    0",
    # "2      1     1       6    0    0    1",
    # "       2     1       0   10    8    0",
    # "       3     9       0    8    8    0",
    # "3      1     4       6    0    0    5",
    # "       2     5       0   10    5    0",
    # "      3     7       0   10    0    4",
    # ...]
    #
    #output:      _duration
    # {'1': {'1'; 0}, '2': {'1': 1, '2': 1, '3': 9}, '3'},
    def to_int_on_the_position(line, position):
        return int(line[position])
    return find_modes_lines_generic(list_of_lines, to_int_on_the_position)


def find_modes_demand(list_of_lines):
    #list_of_paragraph_lines:
    #["1      1     0       0    0    0    0",
    # "2      1     1       6    0    0    1",
    # "       2     1       0   10    8    0",
    # "       3     9       0    8    8    0",
    # "3      1     4       6    0    0    5",
    # "       2     5       0   10    5    0",
    # "      3     7       0   10    0    4",
    # ...]
    #
    #output:
    # {'1': {'1'; [0, 0, 0, 0]}, '2': {'1': [6, 0, 0, 1], '2': [0, 10, 8, 0], '3': [0, 8, 8, 0]}, ...}
    def map_tokens_to_list_of_ints_from_postion_to_end(line, position):
        return [int(x) for x in line[position+1:]]
    return find_modes_lines_generic(list_of_lines, map_tokens_to_list_of_ints_from_postion_to_end)


def read_modes_paragraph(list_of_paragraph_lines):
    pass
    #list_of_paragraph_lines:
    #["REQUESTS/DURATIONS:",
    #"jobnr. mode duration  R 1  R 2  N 1  N 2",
    #"------------------------------------------------------------------------",
    #"1      1     0       0    0    0    0",
    # "2      1     1       6    0    0    1",
    # "       2     1       0   10    8    0",
    # "       3     9       0    8    8    0",
    # "3      1     4       6    0    0    5",
    # "       2     5       0   10    5    0",
    # "      3     7       0   10    0    4",
    # ...]
    #
    #output:
    # ['R1','R2','N1','N2'],
    # {'1': {'1'; 0}, '2': {'1': 1, '2': 1, '3': 9}, ...},
    # {'1': {'1'; [0, 0, 0, 0]}, '2': {'1': [6, 0, 0, 1], '2': [0, 10, 8, 0], '3': [0, 8, 8, 0]}, ...},
    #pass
    labels = parse_modes_paragraph_header(list_of_paragraph_lines[1])
    duration_assignment = find_modes_duration(list_of_paragraph_lines[3:])
    demand = find_modes_demand(list_of_paragraph_lines[3:])
    return labels, duration_assignment, demand
    #return labels, duration_assignment


def find_resources_prefixes_paragraph(list_of_paragraph_lines):
    RESOURES_TAG = "RESOURCES"
    def lines_from_the_first_line_containing_RESOURCES_TAG():
        found = False
        for l in list_of_paragraph_lines:
            if found:
                yield l
            if RESOURES_TAG in l:
                found = True
    return find_resources_prefixes(lines_from_the_first_line_containing_RESOURCES_TAG())

def read_resources_paragraph(list_of_paragraph_lines):
    return read_resources(list_of_paragraph_lines[1], list_of_paragraph_lines[2])

def split_list_of_strings_by_predicate(list_of_lines, predicate):
    result = []
    temporary_buffer = []

    for number, l in enumerate(list_of_lines):
        if predicate(l):
            result.append(temporary_buffer)
            temporary_buffer = []
        else:
            temporary_buffer.append(l)
    result.append(temporary_buffer)
    return [l for l in result if l != []]

def make_activities_dictionary(resource_labels, res_prefixes, duration_assignment, demand_assignment):
    activity_dictionary = {}
    for activity, duration_dictionary in duration_assignment.iteritems():
        demand_dictionary = demand_assignment[activity]
        mode_list = []
        for mode_name in duration_dictionary:
            mode_duration = duration_dictionary[mode_name]
            mode_demand = demand_dictionary[mode_name]
            demand = {key: value for key, value in zip(resource_labels, mode_demand)}
            #TODO: high coupling with find_resources_prefixes_function, remove it
            renewable_demand, non_renewable_demand, doubly_constrained = split_dictionary(demand, res_prefixes)
            if doubly_constrained:
                #TODO: implement doubly constrained resources
                raise AssertionError('Doubly constrained resources not implemented')
            mode_list.append(MultiModeClasses.Mode(mode_name, mode_duration, renewable_demand, non_renewable_demand))
        activity_dictionary[activity] = MultiModeClasses.Activity(activity, mode_list)
    return activity_dictionary


def get_activity_or_raise_parsing_error(activity_dictionary, label, end_label):
    if label == end_label:
        return MultiModeClasses.Activity.DUMMY_END
    try:
        return activity_dictionary[label]
    except KeyError:
        raise PSPLibParsingError("source is not starting, and cannot be found in activity dictionary")

def make_activity_graph(graph, start, stop, activity_dictionary):
    activity_graph = {}
    for source, ends in graph.iteritems():
        if source == start:
            source_activity = MultiModeClasses.Activity.DUMMY_START
        else:
            source_activity = get_activity_or_raise_parsing_error(activity_dictionary, source, stop)

        endlist = [get_activity_or_raise_parsing_error(activity_dictionary, label, stop) for label in ends]

        activity_graph[source_activity] = endlist
    return activity_graph

class PSPLibReader(object):
    def read(self, filename):
        with open(filename, "r") as projectFile:
            paragraphs = split_list_of_strings_by_predicate(projectFile, lambda x : '****' in x)
            res_prefixes = find_resources_prefixes_paragraph(paragraphs[1])
            graph, start, stop = read_precedence_paragraph(paragraphs[3])
            resource_labels, duration_assignment, demand_assignment = read_modes_paragraph(paragraphs[4])
            resource_supply_dictionary = read_resources_paragraph(paragraphs[5])
            activity_dictionary = make_activities_dictionary(resource_labels, res_prefixes, duration_assignment,
                                                             demand_assignment)
            activity_graph = make_activity_graph(graph, start, stop, activity_dictionary)
            #TODO: high coupling with find_resources_prefixes function
            renewable_demand, non_renewable_demand, doubly_constrained = split_dictionary(resource_supply_dictionary, res_prefixes)
            if doubly_constrained:
                raise AssertionError('No support for doubly constrained resources')
            #TODO: implement doubly constrained resources
            return MultiModeClasses.Problem(activity_graph, renewable_demand, non_renewable_demand)
