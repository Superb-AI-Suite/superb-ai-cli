import click
import time
from multiprocessing import Process, Queue

from spb_cli.labels.base_service import BaseService
from spb_cli.labels.exceptions import (
    NotSupportedProjectException
)
from spb_cli.labels.utils import (
    recursive_glob_label_files,
)


class UploadLabelService(BaseService):
    MAX_RETRY_COUNT = 3
    def build_image_labels(
        self
    ):
        pass

    def upload_label(
        self,
        project_name: str,
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
            labels = recursive_glob_label_files(directory_path)
        else:
            raise NotSupportedProjectException(
                "This project is not supported. Please check the project type."
            )

        if len(labels) == 0:
            click.echo("No label files found in the directory.")
            return
        else:
            click.echo(f"2. Found {len(labels)} label files.")
        
        if not is_forced:
            if click.confirm(
                f"Uploading {len(labels)} label files to the project. Proceed?",
            ):
                return
        
        labels_queue = Queue()
        success_queue = Queue()
        fail_queue = Queue()

        # Enuqueue labels for processor
        for label in labels:
            labels_queue.put(label)
        finall_num_process = min(num_process, len(labels))
        for _ in range(finall_num_process):
            labels_queue.put(None)

        click.echo(f"3. Start uploading {len(labels)} label files to the project.")

        # Make worker processors
        worker_processors = []
        for i in range(finall_num_process):
            worker_processors.append(
                Process(
                    target=self.upload_label_worker,
                    args=(i, labels_queue, success_queue, fail_queue),
                )
            )

    def upload_label_worker(
        self,
        worker_id: int,
        labels_queue: Queue,
        success_queue: Queue,
        fail_queue: Queue,
    ):
        click.echo(f"  Worker {worker_id} is started.")
        time.sleep(1)

        while True:
            label_file_config = labels_queue.get()
            if label_file_config is None:
                break
            is_success = True
            try:
                print(label_file_config)
                success_queue.put(label_file_config)
            except:
                is_success = False
                fail_queue.put(label_file_config)


# superb upload labels -p SDKUploadTest -d ./workspace/images -np 4 -y