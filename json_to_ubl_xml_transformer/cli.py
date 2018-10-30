# -*- coding: utf-8 -*-

"""Console script for json_to_ubl_xml_transformer."""
import sys

import click


@click.command()
def main(args=None):
    """Console script for json_to_ubl_xml_transformer."""
    click.echo(
        "Replace this message by putting your code into "
        "json_to_ubl_xml_transformer.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
