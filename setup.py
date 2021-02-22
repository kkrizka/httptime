#!/usr/bin/env python

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='httptime',
    version='0.1.0',
    description='Module for timing http queries inside a python program.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kkrizka/httptime",
    author="Karol Krizka",
    author_email="kkrizka@gmail.com",
    packages=[
        'httptime'
        ]
)
