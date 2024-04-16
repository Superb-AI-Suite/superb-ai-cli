import click

from .describes import describe
from .downloads import download
from .uploads import upload


@click.group()
def label():
    """Label Service CLI"""
    pass


label.add_command(describe)
label.add_command(download)
label.add_command(upload)


__all__ = (
    "label",
)
