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

    def test_validate_valid_numeric(self):
        header = ['act_num', 'tax_yr', 'home_val']
        data = [[1, 2020, 100],
                [1, 2019, 99],
                ]
        csv_file = self.create_csv(header, data)
        parser = TableParser(csv_file)
        parsed_rows = list(parser.read())
        self.assertTrue(parsed_rows)
        self.assertFalse(parser.errors)
        for expected, parsed in zip(data, parsed_rows):
            for expected_val, col in zip(expected, header):
                self.assertEqual(parsed[col], expected_val)

    def test_null_coercion(self):
        header = ['txt_field', 'val']
        data = [['', '']]
        csv_file = self.create_csv(header, data)
        parser = TableParser(csv_file)
        parsed_rows = list(parser.read())
        self.assertTrue(parsed_rows)
        self.assertFalse(parser.errors)
        parsed = parsed_rows[0]
        self.assertEqual(parsed['txt_field'], '')
        self.assertIsNone(parsed['val'])

    def test_coerce_date(self):
        header = ['build_dt']
        data = [['01/01/2020'],
                [''],
                ]
        csv_file = self.create_csv(header, data)
        parser = TableParser(csv_file)
        parser.validate()
        self.assertFalse(parser.errors)

    def test_validate(self):
        header = ['tax_yr']
        data = [[1999],
                ['1-96'],
                ]
        csv_file = self.create_csv(header, data)
        parser = TableParser(csv_file)
        parser.validate(max_row=3)
        self.assertTrue(parser.errors)

    def test_str_maxlength(self):
        header = ['tax_cd']
        data = [['-' * 10_000],
                ['14X80 79 CENTURIAN S#747514T3BB76'],
                ]
        csv_file = self.create_csv(header, data)
        parser = TableParser(csv_file)
        parser.validate()
        self.assertTrue(parser.errors)
        self.assertEqual(len(data), len(parser.errors))
