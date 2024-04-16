import click

from .downloads import DownloadService


@click.command()
@click.option(
    '-d', '--dir', 'directory_path',
    default='.',
    help='Target directory path (default=[./])'
)
@click.option(
    '-p', '--project', 'project_name',
    help='Target project name'
)
@click.option(
    '-y', '--yes', 'is_forced',
    required=False,
    default=False,
    help='Say YES to all prompts',
    is_flag=True
)
@click.option(
    '-np', '--num_process', 'num_process',
    type=int,
    required=False,
    default=2,
    help='Number of processors for executing commands (default=2)'
)
def download(
    project_name,
    directory_path,
    is_forced,
    num_process,
):
    """Download all data and labels of your project in Superb Platform """
    if num_process < 1:
        print("[ERROR] num_process must be more than 0.")
        return

    if num_process > 10:
        print("[ERROR] num_process must be less than 11.")

    if project_name is None:
        print("[ERROR] You have to pass project name for this command")
        return

    service = DownloadService()
    service.download(
        project_name=project_name,
        directory_path=directory_path,
        is_forced=is_forced,
        num_process=num_process,
    )


__all__ = (
    "download",
)
