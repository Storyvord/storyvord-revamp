from google.cloud import storage
import mimetypes
from google.oauth2 import service_account

def upload_to_project_files_bucket(file, bucket_name, project_folder):
    client = storage.Client(credentials=service_account.Credentials.from_service_account_file(
        r'D:\DjangoStoryVordRE-2024\storyvord-revamp\storyvord\apis-gcp-storyvord.json'))
    bucket = client.bucket(bucket_name)  # Use the passed bucket name
    destination_path = f"{project_folder}{file.name}"  # Destination path in the bucket
    blob = bucket.blob(destination_path)
    content_type, _ = mimetypes.guess_type(file.name)
    content_type = content_type or 'application/octet-stream'
    try:
        blob.upload_from_string(file.read(), content_type=content_type)
        print(f"File uploaded successfully to {bucket_name}/{destination_path}")
    except Exception as e:
        print(f"Error uploading file to {bucket_name}/{destination_path}: {e}")
