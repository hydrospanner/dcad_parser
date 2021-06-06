import io
import unittest

from ..metadata_parser import DcadTablesParser


class TableParserTests(unittest.TestCase):

    def create_table_file(self, table_fields):
        table_file = io.StringIO()
        for table_name, columns in table_fields.items():
            table_file.write(
                f'{DcadTablesParser.TABLE_STARTSWITH}[{table_name}]\n')
            for col_name in columns:
                table_file.write(f'[{col_name}]\n')
            table_file.write('\n')
        table_file.seek(0)
        return table_file

    def test_read(self):
        tables = {
            'account': ['account_id', 'name'],
            'tax_assessment': ['account_id', 'tax_yr'],
        }
        table_file = self.create_table_file(tables)
        parser = DcadTablesParser(table_file)
        table_iterator = zip(parser.metadata.tables.values(), tables.items())
        for table, (tbl_name, cols) in table_iterator:
            self.assertEqual(table.name, tbl_name)
            for column, expected_col in zip(table.columns.values(), cols):
                self.assertEqual(column.name, expected_col)

    def test_col_before_table(self):
        table_file = io.StringIO()
        table_file.write('[column_name]\n')
        table_file.seek(0)
        with self.assertRaises(ValueError):
            DcadTablesParser(table_file)

    def test_unparsable_line(self):
        table_file = io.StringIO()
        table_file.write(
            f'{DcadTablesParser.TABLE_STARTSWITH}[table_name]\n')
        table_file.write('[column_name\n')
        table_file.seek(0)
        with self.assertRaises(ValueError):
            DcadTablesParser(table_file)
