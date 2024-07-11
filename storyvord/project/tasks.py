from celery import shared_task
from .storage_utils import upload_to_project_files_bucket

@shared_task
def process_and_upload_file(file_path, project_name, bucket_name):
    project_folder = f"projects/{project_name}/uploaded_documents/"
    upload_to_project_files_bucket(file_path, bucket_name, project_folder)
