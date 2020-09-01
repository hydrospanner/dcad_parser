"""Data structures for field name metadata and coercion."""
from sqlalchemy import BOOLEAN, FLOAT, INTEGER, TEXT, DATE


class FieldType:
    """Base class for field data type data."""

    coerce_func = None

    def __init__(self):
        pass

    def coerce_func(self, val):
        if val is '':
            return None
        return self.coerce_to(val)


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
        yn = yn_str.upper()
        if yn == 'Y':
            return True
        elif yn == 'N':
            return False


class StrField(FieldType):

    sqlalchemy_type = TEXT
    cerberus_type = 'string'
    coerce_func = str


class IntField(FieldType):

    sqlalchemy_type = INTEGER
    cerberus_type = 'integer'
    coerce_to = int


class FloatField(FieldType):

    sqlalchemy_type = FLOAT
    cerberus_type = 'float'
    coerce_to = float


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
    INT_SUFFIX = {'YR', 'NUM', 'SF', 'ID', 'DIM'}
    FLOAT_SUFFIX = {'PCT', 'MKT', 'TAXABLE', 'AREA', 'AMT', 'VAL'}
    DATE_SUFFIX = {'DT'}
    PK_COLS = {'APPRAISAL_YR', 'ACCOUNT_NUM', 'EXEMPTION_CD',
               'OWNER_SEQ_NUM', 'SECTION_NUM', 'TAX_OBJ_ID'}
    # Exceptions to suffix conventions
    str_fields = {'ACCOUNT_NUM', 'GIS_PARCEL_ID', 'BLDG_ID', 'UNIT_ID',
                  'TAX_OBJ_ID', 'NUM_STORIES_DESC'}
    DELIMITER = '_'

    def __init__(self, name):
        """Initalize field name.

        Args:
            name (str): field name 
        """
        self.name = name
        self.type = self.guess_type()
        self.pk = name in self.PK_COLS
        self.nullable = self.type.cerberus_type != 'string' and not self.pk
        self.schema = self.type.cerberus_schema
        self.schema['nullable'] = self.nullable

    def guess_type(self):
        """Guess column type from column name."""
        name_parts = self.name.upper().split(self.DELIMITER)
        suffix = name_parts[-1]
        prefix = name_parts[0]
        if self.name.upper() in self.str_fields:
            return StrField()
        if suffix in self.BOOL_SUFFIX:
            return BoolField()
        elif suffix in self.INT_SUFFIX or prefix in self.INT_SUFFIX:
            return IntField()
        elif suffix in self.FLOAT_SUFFIX:
            return FloatField()
        elif suffix in self.DATE_SUFFIX:
            return DateField()
        else:
            return StrField()
