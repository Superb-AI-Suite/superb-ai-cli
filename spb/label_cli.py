import click


@click.group()
def label():
    pass


@label.group()
def describe():
    pass


@describe.command()
def projects():
    click.echo("List all projects")
