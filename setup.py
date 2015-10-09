#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
import sys

from setuptools import setup, find_packages

# requirements
install_requirements = []

# package informations
with io.open('imdbfetcher/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]$', f.read(),
                        re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with io.open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

with io.open('HISTORY.rst', 'r', encoding='utf-8') as f:
    history = f.read()


setup(name='imdbfetcher',
      version=version,
      license='GPL3',
      description='Fetch imdb information',
      long_description=readme + '\n\n' + history,
      keywords='video movie episode tv show',
      packages=find_packages(),
      install_requires=install_requirements,
)
