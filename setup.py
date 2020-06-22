from setuptools import setup


with open('README.rst', 'r') as file:
    long_description = file.read()

setup(name='directory_to_sql',
      version='0.1.2',
      description='Parse Dallas Central Appriasal District Dataset',
      long_description=long_description,
      url='http://github.com/hydrospanner/dcad_parser',
      author='John Tucker',
      license='MIT',
      packages=['dcad_parser'],
      install_requires=[
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )

