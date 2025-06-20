import asyncio
import json
import uuid
import boto3
import logging
import os
import tempfile
from urllib.parse import unquote_plus
from text_extractor.extract_text import extract_pdf_text

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Event received: {json.dumps(event)}")

    # Validate and extract event details
    try:
        if 'Records' not in event or not event['Records']:
            raise ValueError("No S3 event records found.")

        record = event['Records'][0]['s3']
        bucket_name =  unquote_plus(record['bucket']['name'])
        s3_file_name =  unquote_plus(record['object']['key'])

        logger.info(f"Triggered by file: {s3_file_name}")

        # Prepare download path
        s3 = boto3.client('s3')
        download_filename = f"{uuid.uuid4()}_{os.path.basename(s3_file_name)}"
        tmp_file_path = os.path.join(tempfile.gettempdir(), download_filename)

        # Attempt to download the file
        try:
            s3.download_file(bucket_name, s3_file_name, tmp_file_path)
            logger.info(f"Downloaded file to: {tmp_file_path}")
        except s3.exceptions.ClientError as e:
            logger.error(f"Failed to download file to path {tmp_file_path}, of bucket {bucket_name} and file name {s3_file_name}: {e}")
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "File not found in S3"})
            }

        # Extract text from PDF
        extracted_text = asyncio.run(extract_pdf_text(tmp_file_path))
        logger.info(f"Extracted text (first 200 chars): {extracted_text[:200]}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Text extracted successfully",
                "excerpt": extracted_text[:200]
            })
        }

    except Exception as e:
        logger.error(f"Unhandled exception when attempting to extract the text from s3 file: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"Exception occurred when attempting to extract the text from s3 file": str(e)})
        }
