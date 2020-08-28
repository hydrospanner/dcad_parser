import csv
import io
import unittest

from ..table_parser import TableParser


class TableParserTests(unittest.TestCase):

    def create_csv(self, header, data):
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)
        csv_file.seek(0)
        return csv_file

    def test__validate_valid_numeric(self):
        header = ['act_num', 'tax_yr', 'home_val']
        data = [[1, 2020, 100],
                [1, 2019, 99],
                ]
        csv_file = self.create_csv(header, data)
        parser = TableParser(csv_file)
        parser.parse()
        self.assertTrue(parser.rows)
        parser.validate()
        self.assertFalse(parser.errors)
        for expected, parsed in zip(data, parser.rows):
            for expected_val, col in zip(expected, header):
                self.assertEqual(parsed[col], expected_val)
