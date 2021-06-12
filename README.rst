Dallas Central Appraisal District Parser
========================================

.. image:: https://travis-ci.com/hydrospanner/dcad_parser.svg?branch=master
    :target: https://travis-ci.com/hydrospanner/dcad_parser

This repo provides tools for fast DB integration of data from the
Dallas Central Appraisal District (DCAD). This includes

- A CLI to generate SQLAlchemy models
  by parsing a data dictionary and ``flask-sqlacodegen``.
- A parser for DCAD's table exports for parsing, coersion, and validation.


Data Model CLI
--------------
Parse the Dallas Central Appraisal District (DCAD) data dictionary into
`sqlalchemy` metadata. Use the generated metadata to generate
Flask-SQLAlchemy model code, using ``flask-sqlacodegen``.


This will convert this data dictionary structure::

    TABLE [ABATEMENT_EXEMPT]                Table containing information for abatement if applicable
            [ACCOUNT_NUM]                   The DCAD Account number
            [APPRAISAL_YR]                  The appraisal year for the data
            [TOT_VAL]                       The total value for the property

into

.. code-block:: python

    from flask_sqlalchemy import SQLAlchemy
    
    
    db = SQLAlchemy()
    
    
    
    class AbatementExempt(db.Model):
        __tablename__ = 'abatement_exempt'
    
        account_num = db.Column(db.Integer, primary_key=True, nullable=False, info='The DCAD Account number')
        appraisal_yr = db.Column(db.Integer, primary_key=True, nullable=False, info='The appraisal year for the data')
        tot_val = db.Column(db.Float, info='The total value for the property')

Example (using the entery point)

.. code-block:: bash

    generate_sqlalchemy path/to/file.txt --outfile models.py --flask

To see the full list of options

.. code-block:: bash

    generate_sqlalchemy --help


Table Parser
------------
This parser functions as a dictionary parser for the invidual table exports.
It also coerces and validates the data.
It uses the same naming convention logic to identify field types as the Data Model process.


Where to get it
---------------
[PyPI](https://pypi.org/project/dcad-parser-hydrospanner/)


.. code-block:: bash

  pip install dcad-parser-hydrospanner
