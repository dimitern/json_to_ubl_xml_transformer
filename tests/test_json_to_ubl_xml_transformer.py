#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `json_to_ubl_xml_transformer` package."""
import os
from collections import OrderedDict

import pytest
from click.testing import CliRunner
from lxml import etree
from xmldiff.main import diff_trees

from json_to_ubl_xml_transformer import cli, json_to_ubl_xml_transformer
from json_to_ubl_xml_transformer.json_to_ubl_xml_transformer import (
    intermediate_json_to_xml,
    load_json,
)

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


def check_attrs(input_parent, intermediate_parent):
    if isinstance(input_parent, dict):
        assert isinstance(intermediate_parent, dict)

        if "__text" in input_parent:
            assert "@value" in intermediate_parent
            assert intermediate_parent["@value"] == input_parent["__text"]

        for key in input_parent:
            if key.startswith("_") and not key.startswith(("__", "@")):
                unprefixed_key = key[1:]
                assert "@attrs" in intermediate_parent
                assert unprefixed_key in intermediate_parent["@attrs"]
                assert (
                    intermediate_parent["@attrs"][unprefixed_key] == input_parent[key]
                )

            elif not key.startswith(("_", "@")) and isinstance(input_parent[key], dict):
                cbc_key = "cbc:%s" % key
                cac_key = "cac:%s" % key
                assert cbc_key in intermediate_parent or cac_key in intermediate_parent

                check_attrs(
                    input_parent[key],
                    intermediate_parent.get(cbc_key, intermediate_parent.get(cac_key)),
                )


@pytest.mark.parametrize(
    "input_json,intermediate_json",
    [
        (
            os.path.join(INPUTS_DIR, "example1.json"),
            os.path.join(INTERMEDIATES_DIR, "example1.json"),
        ),
        (
            os.path.join(INPUTS_DIR, "example2.json"),
            os.path.join(INTERMEDIATES_DIR, "example2.json"),
        ),
    ],
)
def test_input_to_intermediate(input_json, intermediate_json):
    """Test the given input JSON is transformed to expected JSON intermediate output."""

    input_data = load_json(input_json)
    intermediate_data = load_json(intermediate_json)

    assert len(input_data) == len(intermediate_data) == 1
    assert set(input_data.keys()) == set(intermediate_data.keys()) == set(["Invoice"])
    assert set(input_data.keys()) == set(["Invoice"])

    assert "@attrs" not in input_data["Invoice"]
    assert "@attrs" in intermediate_data["Invoice"]
    assert intermediate_data["Invoice"]["@attrs"] == OrderedDict(
        [
            (
                "xmlns:cac",
                "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            ),
            (
                "xmlns:cbc",
                "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            ),
            ("xmlns", "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"),
        ]
    )

    assert "cbc:CustomizationID" in intermediate_data["Invoice"]
    assert "cbc:CustomizationID" not in input_data["Invoice"]
    assert (
        intermediate_data["Invoice"]["cbc:CustomizationID"]
        == "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
    )

    assert "cbc:ProfileID" in intermediate_data["Invoice"]
    assert "cbc:ProfileID" not in input_data["Invoice"]
    assert (
        intermediate_data["Invoice"]["cbc:ProfileID"]
        == "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
    )

    invoice = intermediate_data["Invoice"]
    for key in input_data["Invoice"]:
        cbc_key = "cbc:%s" % key
        cac_key = "cac:%s" % key
        value = input_data["Invoice"][key]

        if isinstance(value, dict):
            assert cbc_key in invoice or cac_key in invoice

            check_attrs(value, invoice.get(cbc_key, invoice.get(cac_key)))

        elif isinstance(value, (list, tuple)):
            count = len(value)
            for i in range(count):
                suffix = "__%d" % i
                assert cbc_key + suffix in invoice or cac_key + suffix in invoice

                child = invoice.get(cbc_key + suffix, invoice.get(cac_key + suffix))
                assert "@name" in child
                assert child["@name"] in (cbc_key, cac_key)


@pytest.mark.parametrize(
    "intermediate_json,output_xml",
    [
        (
            os.path.join(INTERMEDIATES_DIR, "example1.json"),
            os.path.join(OUTPUTS_DIR, "example1.xml"),
        ),
        (
            os.path.join(INTERMEDIATES_DIR, "example2.json"),
            os.path.join(OUTPUTS_DIR, "example2.xml"),
        ),
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
    assert "Usage: json_to_ubl_xml_transformer [OPTIONS] INPUTS" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "-h, --help" in help_result.output
    assert "Show this message and exit." in help_result.output
