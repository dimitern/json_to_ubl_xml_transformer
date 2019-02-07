# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import absolute_import, print_function, unicode_literals

import codecs
import json
import re
from collections import OrderedDict

import six
from xmler import dict2xml

from json_to_ubl_xml_transformer.constants import DEFAULT_ENCODING, FALLBACK_ENCODING


def escape_utf_8_chars(input_text):
    """
    Escapes characters like "\xe4" with "\u00e4".
    Only necessary to support Python 2.7+.
    """
    ascii_text = six.binary_type()
    for c in input_text:
        encoded = c.encode("utf-8")
        if len(encoded) != 1:
            for b in bytearray(encoded):
                ascii_text += six.b(r"\\u00" + "%x" % b)
        else:
            ascii_text += six.b(c)
    return codecs.decode(ascii_text, "utf-8")


def unescape_utf_8_chars(input_text):
    """
    Unescapes characters like "\u00e4" with "&#x00e4;".
    Only necessary to support Python 2.7+.
    """
    pattern = re.compile(r"\\u00(\w{2})")

    def replace(match):
        return "&#x" + match.group()[2:] + ";"

    return pattern.sub(replace, input_text)


def replace_unescaped_utf_8_chars(input_text):
    """
    Unescapes characters like "&#x00c3;&#x00a4;" with their equivalents,
    e.g. "ö". Only necessary to support Python 2.7+.
    """
    pattern = re.compile(r"&#x00(\w{2});&#x00(\w{2});")

    def replace(match):
        byte_array = bytearray(map(lambda v: int(v, 16), match.groups()))
        return byte_array.decode("utf-8")

    return pattern.sub(replace, input_text)


def load_json(input_file):
    """
    Loads the given `input_file` filename as JSON and returns the result.
    """

    with codecs.open(input_file, "rb") as f:
        input_data = f.read()
        if input_data[:3] == codecs.BOM_UTF8:
            input_text = input_data.decode(FALLBACK_ENCODING)
        else:
            input_text = input_data.decode(DEFAULT_ENCODING)

        return json.loads(
            escape_utf_8_chars(input_text),
            object_hook=OrderedDict,
            object_pairs_hook=OrderedDict,
        )


def intermediate_json_to_xml(intermediate_json, output_xml=None):
    """
    Reads the given `intermediate_json` filename as JSON, and
    transforms its content to equivalent XML, saving the result
    in `output_xml` (a file-like object or a string filename),
    or if the latter is None, returns the XML as string.
    """

    if isinstance(intermediate_json, six.string_types):
        parsed_json = load_json(intermediate_json)
    else:
        parsed_json = intermediate_json

    output = replace_unescaped_utf_8_chars(
        unescape_utf_8_chars(
            dict2xml(parsed_json, encoding=DEFAULT_ENCODING, pretty=True)
        )
    )

    if output_xml is None:
        return output

    output_xml = (
        codecs.open(output_xml, "wb", encoding=DEFAULT_ENCODING)
        if isinstance(output_xml, six.string_types)
        else output_xml
    )

    output_xml.write(output)
    output_xml.flush()
    output_xml.close()
