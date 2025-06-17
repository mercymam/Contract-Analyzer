import asyncio
import json
import uuid
import boto3
import logging
import os
import tempfile

from text_extractor.extract_text import extract_pdf_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    logger.info(json.dumps(event))

    if 'Records' not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No S3 event records found."})
        }

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')
    tmp_file_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_{os.path.basename(key)}")

    s3.download_file(bucket, key, tmp_file_path)
    logger.info(f"Downloaded {key} to {tmp_file_path}")

    extracted_text = asyncio.run(extract_pdf_text(tmp_file_path))
    logger.info(f"Extracted text: {extracted_text[:200]}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Text extracted", "text_excerpt": extracted_text[:200]})
    }
