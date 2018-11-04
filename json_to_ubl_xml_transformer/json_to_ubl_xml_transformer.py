# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import print_function, unicode_literals

import codecs
import json
import re
from collections import OrderedDict

import six
from xmler import dict2xml

DEFAULT_ENCODING = "utf-8"
FALLBACK_ENCODING = "utf-8-sig"


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
    return ascii_text


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


def intermediate_json_to_xml(intermediate_json, output_xml=None):
    with codecs.open(intermediate_json, "rb") as f:
        input_data = f.read()

        try:
            encoding = json.detect_encoding(input_data)
        except AttributeError:
            try:
                encoding = FALLBACK_ENCODING
                input_data.decode(encoding)
            except ValueError:
                encoding = DEFAULT_ENCODING
                input_data.decode(encoding)

        input_text = escape_utf_8_chars(input_data.decode(encoding))
        input_data = six.binary_type(input_text)

        parsed_json = json.loads(
            input_data.decode(DEFAULT_ENCODING),
            object_hook=OrderedDict,
            object_pairs_hook=OrderedDict,
        )

        output = replace_unescaped_utf_8_chars(
            unescape_utf_8_chars(
                dict2xml(parsed_json, encoding=DEFAULT_ENCODING, pretty=True)
            )
        )

        if not output_xml:
            return output

        output_xml.write(output)
        output_xml.flush()
        output_xml.close()
