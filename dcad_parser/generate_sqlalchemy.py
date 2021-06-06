"""Generate Flask SQLAlchemy models from DCAD data dictionary."""
import argparse
import sys

from sqlacodegen.codegen import CodeGenerator

from dcad_parser.parser.metadata_parser import DcadTablesParser


def main():
    parser = argparse.ArgumentParser(
        description='Generate Flask SQLAlchemy models from DCAD data '
                    'dictionary.')
    parser.add_argument('input_path', nargs='?',
                        help='DCAD data dictionary file')
    parser.add_argument('--noindexes',
                        action='store_true', help='ignore indexes')
    parser.add_argument('--nojoined', action='store_true',
                        help="don't autodetect joined table inheritance")
    parser.add_argument(
        '--noinflect', action='store_true',
        help="don't try to convert tables names to singular form")
    parser.add_argument(
        '--noclasses', action='store_true',
        help="don't generate classes, only tables")
    parser.add_argument(
        '--outfile',
        help='file to write output to (default: stdout)')
    parser.add_argument(
        '--nobackrefs', action='store_true',
        help="don't include backrefs")
    parser.add_argument(
        '--flask', action='store_true',
        help="use Flask-SQLAlchemy columns")
    parser.add_argument(
        '--ignore-cols',
        help="don't check foreign key constraints on "
             "specified columns (comma-separated)")
    parser.add_argument(
        '--nocomments', action='store_true',
        help="don't render column comments")
    args = parser.parse_args()

    with open(args.input_path, encoding='ISO-8859-1') as tbl_file:
        parser = DcadTablesParser(tbl_file)
    ignore_cols = args.ignore_cols.split(',') if args.ignore_cols else None
    generator = CodeGenerator(parser.metadata,
                              noconstraints=True,
                              noindexes=args.noindexes,
                              nojoined=args.nojoined,
                              noinflect=args.noinflect,
                              nobackrefs=args.nobackrefs,
                              flask=args.flask,
                              ignore_cols=ignore_cols,
                              noclasses=args.noclasses,
                              nocomments=args.nocomments,
                              )
    if args.outfile:
        with open(args.outfile, 'w') as outfile:
            generator.render(outfile)
    else:
        generator.render(sys.stdout)


if __name__ == '__main__':
    main()
