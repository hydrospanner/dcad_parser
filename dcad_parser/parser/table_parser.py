"""Parser for CSV table data."""

import csv

from cerberus import Validator

from .metadata_parser import FieldName


class TableParser:
    """Parse the csv files of table data."""

    def __init__(self, parse_file):
        """Initalize parser.

        Args:
            parse_file (file-like object):
                File to parse
        """
        self.parse_file = parse_file
        self.rows = []
        self.errors = {}

    def parse(self):
        reader = csv.DictReader(self.parse_file)
        for row in reader:
            row['line_num'] = reader.line_num
            self.rows.append(row)

    def validate(self):
        # Use the field names to determine the correct schema to validate against
        # create schema from row keys(blank if rows are missing)
        if not self.rows:
            return
        row_schema = {field: FieldName(field).schema for
                      field in self.rows[0].keys()}
        validator = Validator(row_schema)
        for row in self.rows:
            validated = validator.validated(row)
            if validated:
                # replace normalized data
                pass
            else:
                self.errors[row['line_num']] = validator.errors
