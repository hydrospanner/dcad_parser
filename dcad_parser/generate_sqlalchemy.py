import sys
from sqlalchemy import Table, MetaData
from sqlacodegen.codegen import CodeGenerator

from .table_parser import DcadTablesParser


f_path = '/home/jt/Downloads/DCAD/DCAD2020_CURRENT/TABLES AND FIELD NAMES.TXT'
parser = DcadTablesParser(f_path)

outfile = sys.stdout
generator = CodeGenerator(parser.metadata, noconstraints=True, flask=True)
generator.render(outfile)
