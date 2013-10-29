from unittest import TestCase
from PSPLIBReader import read_precedence_relation, read_resources, split_dictionary, find_resources_prefixes, find_resources_prefixes_paragraph, find_modes_duration


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
#wy:
# ("R", "N", "D")

