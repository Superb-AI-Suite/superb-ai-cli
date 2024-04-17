import click
from multiprocessing import Pool

from spb_cli.labels.base_service import BaseService
from spb_cli.labels.exceptions import (
    NotSupportedProjectException
)
from spb_cli.labels.utils import (
    recursive_glob_image_files,
    divide_list,
)


class UploadDataService(BaseService):
    MAX_RETRY_COUNT = 3

    def build_image_assets(
            self,
            dataset: str,
            directory_path: str,
    ):
        images_path = recursive_glob_image_files(directory_path)
        if len(images_path) == 0:
            return []
        
        return [{
            "file": file_path,
            "data_key": key,
            "dataset": dataset,
        } for key, file_path in images_path.items()]

    def build_video_assets(
            self,
            dataset: str,
            directory_path: str,
    ):
        pass

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
        click.echo(
            "1. Complete describing project."
        )

        if project.workapp == "image-siesta":
            assets = self.build_image_assets(
                directory_path=directory_path,
                dataset=dataset,
            )
            worker = self.upload_image_worker
        elif project.workapp == "video-siesta":
            assets = self.build_video_assets(
                directory_path=directory_path,
                dataset=dataset,
            )
            worker = self.upload_video_worker
        else:
            raise NotSupportedProjectException("Only image and video projects are supported for now.")
        
        if len(assets) == 0:
            click.echo("No data found.")
            return
        else:
            click.echo(f"2. Complete building data. {len(assets)} data is found.")
        
        if not is_forced:
            if not click.confirm(
                f"Uploading {len(assets)} data to project {project.name}. Proceed?"
            ):
                return
        
        click.echo("3. Start uploading data.")
        divided_assets = divide_list(assets, num_process)
        with Pool(
            processes=num_process,
        ) as p:
            results = p.map(
                worker,
                zip(
                    range(num_process),
                    divided_assets,
                )
            )
        success_count = 0
        fail_count = 0
        failed_assets = []
        for result in results:
            success_count += len(result["success"])
            fail_count += len(result["failed"])
            failed_assets += result["failed"]
        
        result_summary = f"Trying: {len(assets)} Success: {success_count}, Fail: {fail_count}"
        click.echo(
            f"4. Complete uploading data. {result_summary}."
        )
    
    def upload_image_worker(
            self,
            params,
    ):
        success_list = []
        failed_list = []
        [process_num, assets] = params
        print(len(assets))
        for asset in assets:
            is_success = False
            try:
                result = self.client.upload_image(
                    path=asset["file"],
                    key=asset["data_key"],
                    dataset_name=asset["dataset"],
                )
                if result:
                    is_success = True
                    success_list.append(asset)
                else:
                    is_success = False
                    failed_list.append(asset)
            except Exception as e:
                is_success = False
                failed_list.append(asset)
            message = f"[{asset['file']}] to [{asset['dataset']}] dataset"
            click.echo(
                f"    Uploading... : {'Success' if is_success else 'Fail'} {message}."
            )

        success_list = assets
        return {
            "success": success_list,
            "failed": failed_list,
        }
    
    def upload_video_worker(
            self,
            params,
    ):
        print(params)


# superb upload dataset -p SDKUploadTest -d ./workspace/images -np 4 -y -n 1