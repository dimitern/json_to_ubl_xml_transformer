from __future__ import absolute_import
from copy import deepcopy
import codecs
import json
from collections import OrderedDict

import six

from json_to_ubl_xml_transformer.constants import (
    ATTRIBUTE_PREFIX,
    ATTRIBUTES,
    CAC,
    CBC,
    CBC_ELEMENTS,
    DEFAULT_ENCODING,
    LIST_ITEM,
    NAME,
    UBL_INVOICE_ROOT,
    VALUE,
    VALUE_ATTRIBUTE,
)
from json_to_ubl_xml_transformer.json_to_ubl_xml_transformer import escape_utf_8_chars


class JSONTransformer(object):
    def transform_name(self, name, index=None):
        if CBC("") in name or CAC("") in name:
            return name if index is None else LIST_ITEM(name, index)

        if name == VALUE_ATTRIBUTE:
            return VALUE

        if name.startswith(ATTRIBUTE_PREFIX):
            return name[1:]

        if name in CBC_ELEMENTS:
            return CBC(name) if index is None else LIST_ITEM(CBC(name), index)

        return CAC(name) if index is None else LIST_ITEM(CAC(name), index)

    def transform_list(self, parent_name, items):
        base_name = self.transform_name(parent_name)
        entries = OrderedDict()
        for index, item in enumerate(items):
            item_name = self.transform_name(parent_name, index)
            entries[item_name] = OrderedDict(
                [(NAME, base_name)]
                + list(six.iteritems(self.transform_dict(item, index)))
            )
        return entries

    def transform_dict(self, item_dict, index=None):
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
                if ATTRIBUTES not in item_dict:
                    item_dict[ATTRIBUTES] = OrderedDict()

                item_dict[ATTRIBUTES][child_name] = item
                del item_dict[name]

            elif name == VALUE_ATTRIBUTE:
                item_dict[self.transform_name(name)] = item
                del item_dict[name]

            elif isinstance(item, list):
                for list_item_name, list_item in six.iteritems(
                    self.transform_list(child_name, item)
                ):
                    item_dict[list_item_name] = list_item
                del item_dict[name]

            elif isinstance(item, dict):
                item_dict[child_name] = self.transform_dict(item)
                del item_dict[name]

            else:
                assert isinstance(item, six.text_type)
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
                for list_item_name, list_item in six.iteritems(
                    self.transform_list(item_name, item)
                ):
                    invoice[list_item_name] = list_item

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
