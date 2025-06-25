import logging
import os
import tempfile
import uuid
from urllib.parse import unquote_plus

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client('database_communications')

def download_file_path_from_s3(event) -> dict[str, int | str] | str:
    if 'Records' not in event or not event['Records']:
        raise ValueError("No S3 event records found.")

    record = event['Records'][0]['database_communications']
    bucket_name = unquote_plus(record['bucket']['name'])
    s3_file_name = unquote_plus(record['object']['key'])

    logger.info(f"Fetching file from bucket: {bucket_name}, key: {s3_file_name}")

    download_filename = f"{uuid.uuid4()}_{os.path.basename(s3_file_name)}"
    tmp_file_path = os.path.join(tempfile.gettempdir(), download_filename)
    s3.download_file(bucket_name, s3_file_name, tmp_file_path)
    logger.info(f"Downloaded file to: {tmp_file_path}")
    return tmp_file_path

def upload_file_to_s3(bucket_name: str, file_name: str, file_content: bytes, content_type: str = "text/plain") -> None:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content, ContentType=content_type)
        logger.info(f"Uploaded file to S3: {file_name}")
