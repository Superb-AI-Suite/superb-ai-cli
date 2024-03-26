import click

from .describes import describe


@click.group()
def label():
    """Label Service CLI"""
    pass


label.add_command(describe)


@label.group()
def download():
    pass


@label.group()
def upload():
    pass


__all__ = (
    "label",
)
