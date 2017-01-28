# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ml20m_zadatak',
    version='0.1.0',
    description='Jednostavan program za rješavanje ml20 zadatka',
    long_description=readme,
    author='Aldo Zelen',
    author_email='azelen@gmail.com',
    url='https://bitbucket.org/azelen/ml20m_zadatak',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
