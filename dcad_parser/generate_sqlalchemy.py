import argparse
import sys

from sqlalchemy import Table, MetaData
from sqlacodegen.codegen import CodeGenerator

from dcad_parser.table_parser import DcadTablesParser


parser = argparse.ArgumentParser(description='Generates SQLAlchemy model code from DCAD data dictionary.')
parser.add_argument('input_path', nargs='?', help='DCAD data dictionary file')
parser.add_argument('--outfile', help='file to write output to (default: stdout)')
args = parser.parse_args()


with open(args.input_path, encoding='ISO-8859-1') as tbl_file:
    parser = DcadTablesParser(tbl_file)
generator = CodeGenerator(parser.metadata, noconstraints=True, flask=True)
if args.outfile:
    with open(args.outfile, 'w') as outfile:
        generator.render(outfile)
else:
    generator.render(sys.stdout)
