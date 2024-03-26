import io
import json

import click

from spb.labels import label


def load_config():
    with io.open('config.json', 'r', encoding='utf-8') as fid:
        return json.load(fid)


CONFIGS = load_config()


@click.group()
@click.version_option(
    version=CONFIGS["CLI_VERSION"],
    message="Superb Platform CLI. version %(version)s",
)
def cli():
    pass


@cli.command()
def version():
    click.echo(CONFIGS["CLI_VERSION"])


cli.add_command(label)


if __name__ == "__main__":
    cli()
