#!/usr/bin/env python

from setuptools import setup

with open('README.md', 'r') as fh:
    readme = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

VERSION = '0.0.1'

setup(
    name='fillme',
    version=VERSION,
    description='A lightweight library to generate dummy data for database using AI',
    long_description=readme,
    author='Soheil Dolatabadi',
    author_email='soheildolat@gmail.com',
    packages=['fillme'],
    install_requires=requirements
)
