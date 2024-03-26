import click

from typing import Optional

from spb.labels.describes.projects import ProjectService


@click.group()
def label():
    pass


@label.group()
def describe():
    pass


@describe.command()
@click.option(
    "-s",
    "--show",
    "show_options",
    default="default",
    help="Show which information about projects for the given option : (default | reviews)",
)
@click.option(
    "-d",
    "--data",
    "data_type",
    default="all",
    help="Select the project data type to show : (all | image | video | pointcloud)"
)
@click.option(
    "-n",
    "--name",
    "project_name",
    default=None,
    help="The substring to search for within the project name"
)
def projects(
    show_options: str,
    data_type: str,
    project_name: Optional[str],
):
    service = ProjectService()
    service.show_projects(
        show_options, data_type, project_name,
    )


__all__ = (
    "label",
)
