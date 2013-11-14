from unittest import TestCase
from PSPLIBReader import read_precedence_relation, read_resources, split_dictionary, find_resources_prefixes, find_resources_prefixes_paragraph, find_modes_duration, parse_modes_paragraph_header, PSPLibParsingError, read_modes_paragraph, find_modes_demand, split_list_of_strings_by_predicate


__author__ = 'Aleksandra'


class TestRead_precedence_relation(TestCase):
    def test_read_precedence_relation(self):
        l1 = ['1        1          3           2   3   4',
              ' 2        3          2           5  10',
              '10 1 1 11',
              '5 1 1 11',
              '3 1 1 11',
              '4 1 1  11'
             ]

        expected_dict, expected_dummy_start, expected_dummy_end = {'1':['2','3','4'],'2':['5','10'], '10': ['11'],
                                                                   '5': ['11'], '3': ['11'], '4': ['11']}, '1', '11'
        result_dict, result_dummy_start, result_dummy_end = read_precedence_relation(l1)
        self.assertEqual(result_dict, expected_dict)
        self.assertEqual(result_dummy_start, expected_dummy_start)
        self.assertEqual(result_dummy_end, expected_dummy_end)

    def test_read_resources(self):
        label_line = 'R 1  R 2  N 1  N 2'
        capacity_line = '20   26   23   36'
        self.assertEqual(read_resources(label_line, capacity_line), {'R1': 20, 'R2': 26, 'N1': 23, 'N2': 36})

    def test_split_dictionary(self):
        input_dict = {"some1": 4, "some5": 2, "other5": 9}
        list_of_prefixes= ["some","other"]
        self.assertEqual(split_dictionary(input_dict, list_of_prefixes), [{"some1": 4, "some5": 2}, {"other5": 9}])

    def test_find_resources_prefixes(self):
        lines = ["  - renewable                 :  2   R",
            "  - nonrenewable              :  2   N",
            "  - doubly constrained        :  0   D"
            ]
        self.assertEqual(find_resources_prefixes(lines), ['R', 'N', 'D'])

    def test_find_resources_prefixes_paragraph(self):
        lines = ["projects                      :  1",
                 "jobs (incl. supersource/sink ):  18",
                 "horizon                       :  122",
                 "RESOURCES",
                 "  - renewable                 :  2   R",
                 "  - nonrenewable              :  2   N",
                 "  - doubly constrained        :  0   D"]
        self.assertEqual(find_resources_prefixes_paragraph(lines), ['R', 'N', 'D'])

    def test_find_modes_duration(self):
        lines = [" 1      1     0       0    0    0    0",\
                "2      1     1       6    0    0    1",\
                "       2     1       0   10    8    0",\
                "       3     9       0    8    8    0" ]

        expected_result = {'1': {'1': 0}, '2': {'1': 1, '2': 1, '3': 9}}
        self.assertEqual(find_modes_duration(lines), expected_result)

    def test_find_modes_duration_lacking_mode_causes_exception(self):
        lines = [" 1      1     0       0    0    0    0",\
                "2      1     1       6    0    0    1",\
                "             1       0   10    8    0",\
                "       3     9       0    8    8    0" ]

        with self.assertRaises(PSPLibParsingError):
            find_modes_duration(lines)

    def test_parse_modes_paragraph_header(self):
        input_line = "jobnr. mode duration  R 1  R 2  N 1  N 2"
        resource_sequence = parse_modes_paragraph_header(input_line)
        self.assertEqual(resource_sequence, ["R1",  "R2", "N1", "N2"])

    def test_parse_modes_paragraph_header_raise_when_not_known_header(self):
        input_line =  "mode jobnr. duration  R 1  R 2  N 1  N 2"
        with self.assertRaises(PSPLibParsingError):
            parse_modes_paragraph_header(input_line)


    def test_read_modes_paragraph(self):
        list_of_paragraph_lines = ["REQUESTS/DURATIONS:",
                                   "jobnr. mode duration  R 1  R 2  N 1  N 2",
                                   "------------------------------------------------------------------------",
                                   "1      1     0       0    0    0    0",
                                   "2      1     1       6    0    0    1",
                                   "       2     1       0   10    8    0",
                                   "       3     9       0    8    8    0"]
        expected_result = (['R1','R2','N1','N2'],
                           {'1': {'1': 0}, '2': {'1': 1, '2': 1, '3': 9}},
                           {'1': {'1':[0, 0, 0, 0]},
                            '2': {'1': [6, 0, 0, 1], '2': [0, 10, 8, 0], '3': [0, 8, 8, 0]}})

        result = read_modes_paragraph(list_of_paragraph_lines)
        self.assertEqual(result, expected_result)

    def test_find_modes_demand(self):
        lines = [" 1      1     0       0    0    0    0",\
        "2      1     1       6    0    0    1",\
        "       2     1       0   10    8    0",\
        "       3     9       0    8    8    0" ]
        expected_result = {'1': {'1':[0, 0, 0, 0]}, '2': {'1': [6, 0, 0, 1], '2': [0, 10, 8, 0], '3': [0, 8, 8, 0]}}
        self.assertEqual(find_modes_demand(lines), expected_result)

    def test_split_list_of_strings_by_predicate(self):
        lines = ['cfg', '***','ab','cd','***', 'ij', 'kl', '***', 'cfg']
        iters = split_list_of_strings_by_predicate(lines, lambda x : '***' in x)
        self.assertEqual(['cfg'], iters[0])
        self.assertEqual(['ab', 'cd'], iters[1])
        self.assertEqual(['ij', 'kl'], iters[2])
        self.assertEqual(['cfg'], iters[3])



#wy:
# ("R", "N", "D")

