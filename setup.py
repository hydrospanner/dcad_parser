from setuptools import setup, find_packages


with open('README.rst') as file:
    long_description = file.read()

setup(name='dcad-parser-hydrospanner',
      version='0.1.0',
      description='Parse and model Dallas Central Appriasal District data',
      long_description=long_description,
      long_description_content_type='text/x-rst',
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
        'Programming Language :: Python :: 3.8',
      ],
      license='MIT',
      packages=find_packages(),
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
