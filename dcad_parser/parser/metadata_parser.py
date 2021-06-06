"""Parse table names and fields from data dictionary file.

File contains non-UTF-8 characters and has inconsistant syntax between lines.
"""
import re
import string

from sqlalchemy import Column, Table, MetaData

from ..fields import FieldName


class DcadTablesParser:
    """DCAD Table and fields parser.

    Args:
        tbl_file (file-like object):
            file to parse to get table and field data.
    """
    TABLE_STARTSWITH = 'TABLE '

    def __init__(self, tbl_file):
        self.metadata = MetaData()
        self.read(tbl_file)

    def read(self, tbl_file):
        keep_chars = set(string.printable)
        for char in '\n\t':
            keep_chars.remove(char)
        self.current_tbl = None
        for line in tbl_file:
            line = ''.join([c for c in line if c in keep_chars])
            line = line.strip()
            if line.startswith(self.TABLE_STARTSWITH):
                self._add_table(line)
            elif line:
                self._add_column(line)
            else:
                pass

    def _get_bracket_text(self, text):
        bracket_text = re.search(r'\[.*?\]', text)
        if not bracket_text:
            raise ValueError('Cannot find bracket text')
        return bracket_text.group(0)[1:-1]

    def _add_table(self, line):
        """Parse table data."""
        # process table. add it and track it to associate tbl with fields
        tbl_name = self._get_bracket_text(line).lower()
        table = Table(tbl_name, self.metadata,
                      comment=self.get_line_description(line))
        self.current_tbl = table

    def get_line_description(self, line):
        """Get the text after the last tab."""
        return line.split(']')[-1].strip()

    def _add_column(self, line):
        """Parse column data."""
        col_name = self._get_bracket_text(line)
        if self.current_tbl is None:
            raise ValueError('Column {col_name} found before table identified')
        field = FieldName(col_name)
        col = Column(col_name.lower(), field.type.sqlalchemy_type,
                     primary_key=field.pk,
                     comment=self.get_line_description(line))
        self.current_tbl.append_column(col)
