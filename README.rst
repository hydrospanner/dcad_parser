# dcad_parser

Parse the Dallas Central Appraisal District (DCAD) data dictionary into
`sqlalchemy` metadata. From that use `flask-sqlacodegen` to generate
Flask-SQLAlchemy model code.

This will convert this data dictionary structure:
```
TABLE [ABATEMENT_EXEMPT]                Table containing information for abatement if applicable
        [ACCOUNT_NUM]                   The DCAD Account number
        [APPRAISAL_YR]                  The appraisal year for the data
        [TOT_VAL]                       The total value for the property
...
```

into
```
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class AbatementExempt(db.Model):
    __tablename__ = 'abatement_exempt'

    account_num = db.Column(db.Integer, primary_key=True, nullable=False, info='The DCAD Account number')
    appraisal_yr = db.Column(db.Integer, primary_key=True, nullable=False, info='The appraisal year for the data')
    tot_val = db.Column(db.Integer, info='The total value for the property')
...
```

Example:
```
generate_sqlalchemy path/to/file.txt --outfile output/file.py
```

To see the full list of options:
```
generate_sqlalchemy --help
```

