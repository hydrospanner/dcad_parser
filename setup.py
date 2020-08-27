from setuptools import setup


with open('README.rst', 'r') as file:
    long_description = file.read()

setup(name='directory_to_sql',
      version='0.1.2',
      description='Parse Dallas Central Appriasal District Dataset',
      long_description=long_description,
      url='http://github.com/hydrospanner/dcad_parser',
      author='John Tucker',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
      ],
      license='MIT',
      packages=['dcad_parser'],
      install_requires=[
            'flask-sqlacodegen',
            'cerberus',
      ],
      entry_points={
          'console_scripts': [
              'generate_sqlalchemy=dcad_parser.generate_sqlalchemy:main',
          ]
      },
      )
