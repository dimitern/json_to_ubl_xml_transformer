# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import absolute_import, print_function, unicode_literals

import codecs
import json
from collections import OrderedDict

import six
from xmltodict import unparse as dict2xml

from json_to_ubl_xml_transformer.constants import DEFAULT_ENCODING, FALLBACK_ENCODING
from json_to_ubl_xml_transformer import transformers, utils


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
            utils.escape_utf_8_chars(input_text),
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

    output = utils.replace_unescaped_utf_8_chars(
        utils.unescape_utf_8_chars(
            dict2xml(
                parsed_json,
                encoding=DEFAULT_ENCODING,
                pretty=True,
                newl="\n",
                indent="  ",
            )
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


def to_intermediate_json(input_dict, transformer=None):
    """
    Transforms the given `input_dict` using the specified `transformer` (or
    `JSONTransformer` when None), and returns transformed output dict.
    """

    transformer = transformers.JSONTransformer() if transformer is None else transformer
    return transformer.transform(input_dict)
