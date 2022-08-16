from distutils import text_file
from prefect import flow, task
from prefect.filesystems import GCS
from prefect.filesystems import LocalFileSystem

gcs_block = GCS.load('google-storage')


@flow
def print_string():
    local_file_system_block = LocalFileSystem.load('local-block')
    with open('test_file.txt', 'a') as f:
        f.write('hello world\n')
        LocalFileSystem.put_directory(local_file_system_block)

print_string()
