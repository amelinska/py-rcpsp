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
    return result_dict


def tokenize(label_line):
    label_tokens = label_line.split(' ')
    filtered_tokens = [token for token in label_tokens if len(token) > 0]
    return filtered_tokens

#TODO: write tests
def read_resources(label_line, capacity_line):
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
#TODO test for split_dictionary

def find_resources_prefixes(list_of_lines_with_prefixes):
#we:
#["projects                      :  1",
#"jobs (incl. supersource/sink ):  18",
#horizon                       :  122
#RESOURCES
#  - renewable                 :  2   R
#  - nonrenewable              :  2   N
#  - doubly constrained        :  0   D
#]

#wy:
# ("R", "N", "D")


    result_list = []
    for line in resuorces_lines:
        list_of_tokens = line.split(' ')
        filtered_tokens = [token for token in list_of_tokens if len(token)>0]
        resuorce_prefix = filtered_tokens[len(filtered_tokens)-1]
        result_list.append(str(resuorce_prefix))
    return result_list



class PSPLibReader(object):
    def read(self, filename):
        pass