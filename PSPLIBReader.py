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





    pass

class PSPLibReader(object):
    def read(self, filename):
        pass