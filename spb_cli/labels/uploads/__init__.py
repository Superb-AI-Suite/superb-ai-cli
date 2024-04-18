import click

from .upload_data import UploadDataService
from .upload_labels import UploadLabelService


@click.group()
def upload():
    """Upload your data to Superb Platform"""
    pass


@upload.command()
@click.option('-n', '--name', 'name', help='Target dataset name')
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-np', '--num_process', 'num_process', type=int, required=False, default=2, help='Number of processors for executing commands (default=2)')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def dataset(name, project_name, directory_path, num_process, is_forced):
    """Upload data to your Superb Platform project"""
    service = UploadDataService()
    service.upload_data(
        project_name=project_name,
        dataset=name,
        directory_path=directory_path,
        num_process=num_process,
        is_forced=is_forced,
    )


@upload.command()
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-np', '--num_process', 'num_process', type=int, required=False, default=2, help='Number of processors for executing commands (default=2)')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def labels(project_name, directory_path, num_process, is_forced):
    """Upload label json to your Superb Platform project"""
    service = UploadLabelService()
    service.upload_label(
        project_name=project_name,
        directory_path=directory_path,
        num_process=num_process,
        is_forced=is_forced,
    )
