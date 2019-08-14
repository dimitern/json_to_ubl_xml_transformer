from __future__ import absolute_import
from copy import deepcopy
import codecs
import json

import six

from json_to_ubl_xml_transformer.constants import (
    ATTRIBUTE,
    ATTRIBUTE_PREFIX,
    CAC,
    CBC,
    CBC_ELEMENTS,
    DEFAULT_ENCODING,
    UBL_INVOICE_ROOT,
    TEXT_CONTENT,
    VALUE_ATTRIBUTE,
)

from json_to_ubl_xml_transformer.utils import escape_utf_8_chars


class JSONTransformer(object):
    def transform_name(self, name):
        if CBC("") in name or CAC("") in name:
            return name

        if name == VALUE_ATTRIBUTE:
            return TEXT_CONTENT

        if name.startswith(ATTRIBUTE_PREFIX):
            return ATTRIBUTE(name[1:])

        if name in CBC_ELEMENTS:
            return CBC(name)

        return CAC(name)

    def transform_list(self, item_list):
        if not isinstance(item_list, list):
            return item_list

        return [self.transform_dict(item) for item in item_list]

    def transform_dict(self, item_dict):
        if not isinstance(item_dict, dict):
            return item_dict

        if len(item_dict) == 1:
            item_name = list(six.iterkeys(item_dict))[0]
            new_name = self.transform_name(item_name)
            item_dict[new_name] = item_dict[item_name]
            del item_dict[item_name]
            item_dict[new_name] = self.transform_dict(item_dict[new_name])
            return item_dict

        for name, item in six.iteritems(deepcopy(item_dict)):
            child_name = self.transform_name(name)
            if name.startswith(ATTRIBUTE_PREFIX) and name != VALUE_ATTRIBUTE:
                item_dict[child_name] = item
                del item_dict[name]

            elif name == VALUE_ATTRIBUTE:
                item_dict[self.transform_name(name)] = item
                del item_dict[name]

            elif isinstance(item, dict):
                item_dict[child_name] = self.transform_dict(item)
                del item_dict[name]

            elif isinstance(item, list):
                item_dict[child_name] = self.transform_list(item)
                del item_dict[name]

            else:
                item_dict[child_name] = item
                del item_dict[name]

        return item_dict

    def transform(self, input_json, output_json=None):
        root = deepcopy(UBL_INVOICE_ROOT)
        invoice = root["Invoice"]
        for name, item in six.iteritems(input_json["Invoice"]):
            item_name = self.transform_name(name)
            if isinstance(item, dict):
                invoice[item_name] = self.transform_dict(item)

            elif isinstance(item, list):
                invoice[item_name] = self.transform_list(item)

            else:
                invoice[item_name] = item

        if output_json is None:
            return root

        output_json = (
            codecs.open(output_json, "wb", encoding=DEFAULT_ENCODING)
            if isinstance(output_json, six.string_types)
            else output_json
        )

        serialized = escape_utf_8_chars(json.dumps(root, indent=4))

        output_json.write(serialized)
        output_json.flush()
        output_json.close()
