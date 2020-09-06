"""Parser for CSV table data."""

import csv

from cerberus import Validator

from ..fields import FieldName


class TableParser:
    """Parse the csv files of table data."""

    def __init__(self, parse_file, store_rows=False):
        """Initalize parser.

        Args:
            parse_file (file-like object):
                File to parse

        Kwargs:
            store_rows (bool):
                Add the parsed rows to self.rows
        """
        self.parse_file = parse_file
        self.validator = None
        self.errors = {}
        self.store_rows = store_rows
        if store_rows:
            self.rows = []

    def readlines(self):
        """Generae each normalized rows from file."""
        reader = csv.DictReader(self.parse_file)
        for row in reader:
            row = {key.lower(): val for key, val in row.items()}
            row['line_num'] = reader.line_num
            self.validate_row(row)
            yield row

    def parse(self):
        for row in self.readlines():
            if self.store_rows:
                self.rows.append(row)

    def validate_row(self, row):
        if self.validator is None:
            # Use the field names to determine the correct validation schema
            self.row_schema = {field: FieldName(field).schema for
                               field in row.keys()}
            self.validator = Validator(self.row_schema)
        validated = self.validator.validated(row)
        if validated:
            # replace normalized data
            row.update(validated)
        else:
            self.errors[row['line_num']] = self.validator.errors
