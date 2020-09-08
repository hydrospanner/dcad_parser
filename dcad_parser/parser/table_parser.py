"""Parser for CSV table data."""

import csv

from cerberus import Validator

from ..fields import FieldName


class TableParser:
    """Parse the csv files of table data."""

    def __init__(self, parse_file):
        """Initalize parser.

        Args:
            parse_file (file-like object):
                File to parse
        """
        self.parse_file = parse_file
        self.validator = None
        self.errors = {}

    def read(self):
        """Generae each normalized rows from file."""
        reader = csv.DictReader(self.parse_file)
        for row in reader:
            row = {key.lower(): val for key, val in row.items()}
            row['line_num'] = reader.line_num
            self.validate_row(row)
            yield row

    def validate(self, max_row=None):
        """Validate the file.

        Any errors encountered are added to `self.errors`.

        Kwargs:
            max_row (int):
                Stop validation after the line number is parsed.
                Trades better performance for less validation.
        """
        for row in self.read():
            if max_row is not None and row['line_num'] >= max_row:
                break

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
