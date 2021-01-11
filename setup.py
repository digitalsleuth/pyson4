#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="pyson4",
    version="1.0.0",
    author="Corey Forman",
    license="GNU General Public License v3.0",
    url="https://github.com/digitalsleuth/pyson4",
    description=("Firefox jsonlz4 parsing tool"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lz4",
    ],
    scripts=['pyson4.py'],
    package_data={'': ['README.md, LICENSE']},
    include_package_data = True,
)
