# -*- coding: utf-8 -*-

"""Utils module."""
import re

import six
import codecs


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
