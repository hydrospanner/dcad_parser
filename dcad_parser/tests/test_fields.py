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
        }
        for field_name, field_cls in fields.items():
            field = FieldName(field_name)
            self.assertIsInstance(field.type, field_cls)
