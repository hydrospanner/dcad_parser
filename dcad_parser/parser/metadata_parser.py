"""Parse table names and fields from data dictionary file.

File is contains non-UTF-8 characters and has inconsistant syntax between lines.
"""
import os
import re
import string
from datetime import datetime

from sqlacodegen.codegen import CodeGenerator
from sqlalchemy import (BOOLEAN, FLOAT, INTEGER, TEXT, DATE, Column, Table,
                        MetaData)


class FieldType:
    """Base class for field data type data."""

    coerce_func = None

    def __init__(self):
        pass

    @property
    def cerberus_schema(self):
        schema = {'type': self.cerberus_type}
        if self.coerce_func:
            schema['coerce'] = self.coerce_func
        return schema


class BoolField(FieldType):

    sqlalchemy_type = BOOLEAN
    cerberus_type = 'boolean'

    def coerce_func(self, yn_str):
        """Coerce yes/No to boolean."""
        yn = un_str.upper()
        if yn == 'Y':
            return True
        elif yn == 'N':
            return False


class DateField(FieldType):

    sqlalchemy_type = DATE
    cerberus_type = 'datetime'

    def coerce_func(self, dt_str):
        if dt_str:
            return datetime.strptime(dt_str, '%Y/%m/%d')

class FieldName:
    """Parse field schema from field name."""

    # column name suffixes indicating data type
    BOOL_SUFFIX = {'IND'}
    INT_SUFFIX = {'YR', 'NUM', 'SF', 'ID'}
    FLOAT_SUFFIX = {'PCT', 'MKT', 'TAXABLE', 'AREA', 'AMT', 'VAL'}
    DATE_SUFFIX = {'DT'}
    PK_COLS = {'APPRAISAL_YR', 'ACCOUNT_NUM', 'EXEMPTION_CD',
               'OWNER_SEQ_NUM', 'SECTION_NUM'}
    DELIMITER = '_'

    def __init__(self, name):
        self.name = name
        self.sqlalchemy_type = self.guess_type()
        self.pk = name in self.PK_COLS

    def guess_type(self):
        """Guess column type from column name."""
        name_parts = self.name.upper().split(self.DELIMITER)
        suffix = name_parts[-1]
        prefix = name_parts[0]
        if suffix in self.BOOL_SUFFIX:
            return BOOLEAN
        elif any(part in self.INT_SUFFIX for part in name_parts):
            return INTEGER
        elif any(part in self.FLOAT_SUFFIX for part in name_parts):
            return FLOAT
        elif suffix in self.DATE_SUFFIX:
            return DATE
        else:
            return TEXT


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
                continue

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
        field = FieldName(col_name)
        col = Column(col_name.lower(), field.sqlalchemy_type,
                     primary_key=field.pk,
                     comment=self.get_line_description(line))
        self.current_tbl.append_column(col)
