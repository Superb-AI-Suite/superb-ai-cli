import click

from spb.labels.base_service import BaseService
from spb.labels.exceptions import (
    NotSupportedProjectException
)
from spb.labels.utils import (
    recursive_glob_image_files,
)


class UploadDataService(BaseService):
    def upload_data(
        self,
        project_name: str,
        dataset: str,
        directory_path: str = ".",
        num_process: int = 2,
        is_forced: bool = False,
    ):
        self.client.set_project(
            name=project_name,
        )
        project = self.client.project

        if project.workapp == "image-siesta":
            return self.upload_image_data(
                dataset=dataset,
                directory_path=directory_path,
                num_process=num_process,
                is_forced=is_forced,
            )
        elif project.workapp == "video-siesta":
            pass
        else:
            raise NotSupportedProjectException("Only image and video projects are supported for now.")

    def upload_image_data(
        self,
        dataset: str,
        directory_path: str,
        num_process: int,
        is_forced: bool,
    ):
        imgs_path = recursive_glob_image_files(directory_path)
        if len(imgs_path) == 0:
            click.echo("No images found.")
            return

        if not is_forced:
            if not click.confirm(
                f"Uploading {len(imgs_path)} images to project [{self.client.project.name}]. Proceed?"
            ):
                return

        asset_images = []
        for key, file_path in imgs_path.items():
            asset_images.append({
                'file': file_path,
                "data_key": key,
                "dataset": 
            })