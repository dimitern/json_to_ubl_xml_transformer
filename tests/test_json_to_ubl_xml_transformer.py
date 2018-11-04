#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `json_to_ubl_xml_transformer` package."""
import os

from lxml import etree

import pytest
from click.testing import CliRunner
from json_to_ubl_xml_transformer import cli, json_to_ubl_xml_transformer
from json_to_ubl_xml_transformer.json_to_ubl_xml_transformer import (
    intermediate_json_to_xml,
)
from xmldiff.main import diff_trees

INPUTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "inputs"))
INTERMEDIATES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "intermediates")
)
OUTPUTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


@pytest.fixture(scope="session")
def output_xml_file(tmpdir_factory):
    return str(tmpdir_factory.mktemp("outputs").join("output.xml"))


def test_main_docstring():
    """Test the main module docstring."""
    assert json_to_ubl_xml_transformer.__doc__ == "Main module."


@pytest.mark.parametrize(
    "input_json,intermediate_json",
    [
        (
            os.path.join(INPUTS_DIR, "example1.json"),
            os.path.join(INTERMEDIATES_DIR, "example1.json"),
        )
    ],
)
def test_input_to_intermediate(input_json, intermediate_json):
    """Test the given input JSON is transformed to expected JSON intermediate output."""
    pass


@pytest.mark.parametrize(
    "intermediate_json,output_xml",
    [
        (
            os.path.join(INTERMEDIATES_DIR, "example1.json"),
            os.path.join(OUTPUTS_DIR, "example1.xml"),
        )
    ],
)
def test_intermediate_to_output(intermediate_json, output_xml, output_xml_file):
    """Test the given intermediate JSON input is transformed to expected XML output."""

    output_text = intermediate_json_to_xml(intermediate_json, output_xml=None)
    intermediate_json_to_xml(intermediate_json, output_xml=output_xml_file)

    parsed_text = etree.fromstring(output_text.encode("utf-8"))
    parsed_file = etree.parse(output_xml_file).getroot()
    expected_parsed = etree.parse(output_xml).getroot()

    assert diff_trees(parsed_text, parsed_file) == []
    assert diff_trees(parsed_file, expected_parsed) == []


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "json_to_ubl_xml_transformer.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
