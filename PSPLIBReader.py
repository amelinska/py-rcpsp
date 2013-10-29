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
        list_of_tokens = line.split(' ')
        filtered_tokens = [token for token in list_of_tokens if len(token)>0]
        result_dict[filtered_tokens[0]]=filtered_tokens[3:]
    start_end_tuple = find_start_end_tuple(result_dict)
    return (result_dict, start_end_tuple[0], start_end_tuple[1])


def tokenize(label_line):
    label_tokens = label_line.split(' ')
    filtered_tokens = [token for token in label_tokens if len(token) > 0]
    return filtered_tokens

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
    labels = []
    for i in range(0, len(filtered_tokens), 2):
        labels.append(filtered_tokens[i] + filtered_tokens[i+1])

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

def find_resources_prefixes(list_of_lines_with_prefixes):
    #input:
    #       ["  - renewable                 :  2   R",
    #        "  - nonrenewable              :  2   N",
    #        "  - doubly constrained        :  0   D"
    #        ]
    #
    #output:
    # ["R", "N", "D"]

    result_list = []
    for line in list_of_lines_with_prefixes:
        filtered_tokens = tokenize(line)
        resource_prefix = filtered_tokens[len(filtered_tokens)-1]
        result_list.append(str(resource_prefix))
    return result_list

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
    pass



def find_resources_prefixes_paragraph(list_of_paragraph_lines):
    RESOURES_TAG = "RESOURCES"
    def line_generator():
        found = False
        for l in list_of_paragraph_lines:
            if found:
                yield l
            if RESOURES_TAG in l:
                found = True
    return find_resources_prefixes(line_generator())

def read_resources_paragraph(list_of_paragraph_lines):
    return read_resources(list_of_paragraph_lines[1], list_of_paragraph_lines[2])


class PSPLibReader(object):
    def read(self, filename):
        pass