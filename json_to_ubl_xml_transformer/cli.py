# -*- coding: utf-8 -*-

"""Console script for json_to_ubl_xml_transformer."""
from __future__ import absolute_import
import os
import sys

import click
from json_to_ubl_xml_transformer import __version__
from json_to_ubl_xml_transformer.json_to_ubl_xml_transformer import (
    intermediate_json_to_xml,
    load_json,
)
from json_to_ubl_xml_transformer.transformers import JSONTransformer


@click.command(name="json_to_ubl_xml_transformer")
@click.help_option("--help", "-h")
@click.version_option(__version__, "-V", "--version")
@click.argument(
    "input_jsons",
    nargs=-1,
    metavar="INPUTS",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True),
)
@click.option(
    "--output-dir",
    "-O",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True
    ),
    default=None,
    required=False,
    help="Specify output directory for UBL XML files.",
)
@click.pass_context
def main(ctx, input_jsons, output_dir):
    """Console script for json_to_ubl_xml_transformer."""

    if not input_jsons:
        click.echo(ctx.get_help())
        return 0

    for input_json in input_jsons:
        if output_dir is not None:
            output_xml = os.path.join(output_dir, os.path.basename(input_json) + ".xml")
        else:
            output_xml = input_json + ".xml"
        click.echo("\nLoading: %s" % input_json)

        json = load_json(input_json)
        click.echo("Transforming to intermediate JSON...")
        transformer = JSONTransformer()
        intermediate_json = transformer.transform(json)

        click.echo("Transforming to UBL XML: %s" % output_xml)
        intermediate_json_to_xml(intermediate_json, output_xml)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
