import unittest

from ..fields import FieldName
from ..fields import BoolField, DateField, IntField, FloatField, StrField


class TableParserTests(unittest.TestCase):

    def test_guess_type(self):
        # map example field names to their cerberus type
        fields = {
            'pool_ind': BoolField,
            'garage_sf': IntField,
            'sell_dt': DateField,
            'sell_val': FloatField,
            'comment': StrField,
            'num_stories': IntField,
            'num_stories_desc': StrField,
            'pct_complete': FloatField,
            'act_age': IntField,
            'eff_yr_built': IntField,
            'area_uom_desc': StrField,
        }
        for field_name, field_cls in fields.items():
            field = FieldName(field_name)
            msg = (f'"{field_name}" parsed type is {str(field.type)}, expected'
                   f' {field_cls}.')
            self.assertIsInstance(field.type, field_cls,
                                  msg=msg)

    def test_str_schema(self):
        # Test maxlength is set
        field = FieldName('hello_cd')
        self.assertTrue('maxlength' in field.schema)
