#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=6.0"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Dimiter Naydenov",
    author_email="dimiter@naydenov.net",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description=(
        "Converts JSON input files to PEPPOL BIS 3.0 "
        "Invoice UBL XML outputs and validates them"
    ),
    entry_points={
        "console_scripts": [
            "json_to_ubl_xml_transformer=json_to_ubl_xml_transformer.cli:main"
        ]
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="json_to_ubl_xml_transformer",
    name="json_to_ubl_xml_transformer",
    packages=find_packages(include=["json_to_ubl_xml_transformer"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dimitern/json_to_ubl_xml_transformer",
    version="0.1.3",
    zip_safe=False,
)
