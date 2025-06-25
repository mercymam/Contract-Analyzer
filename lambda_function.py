import asyncio
import json
import uuid
import boto3
import logging
import os
import tempfile
from src.data_processing.truncator import truncate_to_fit
from urllib.parse import unquote_plus
from src.text_extractor.extract_text import extract_pdf_text
from src.data_processing.llm import call_llm_api
from src.prompt.prompt import tenancy_analysis_prompt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Event received: {json.dumps(event)}")

    try:
        tmp_file_path = get_file_path_from_s3(event)
        extracted_text = asyncio.run(extract_pdf_text(tmp_file_path))
        logger.info(f"Extracted text (first 200 chars): {extracted_text[:200]}")

        truncated_texts = truncate_to_fit(tenancy_analysis_prompt, extracted_text, "gpt-3.5-turbo", "openai")
        ai_response = ""
        for i, text in enumerate(truncated_texts):
            logger.info(f"Getting the AI response for truncated text: {i}")
            response = call_llm_api(tenancy_analysis_prompt, text)
            if response:
                ai_response += response

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Tenancy contract analyzed successfully",
                "excerpt": ai_response
            })
        }

    except Exception as e:
        logger.error(f"Unhandled exception when attempting to analyze the text from s3 file: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"Exception occurred when attempting to analyze the text from s3 file": str(e)})
        }

def get_file_path_from_s3(event) -> dict[str, int | str] | str:
    if 'Records' not in event or not event['Records']:
        raise ValueError("No S3 event records found.")

    record = event['Records'][0]['s3']
    bucket_name = unquote_plus(record['bucket']['name'])
    s3_file_name = unquote_plus(record['object']['key'])

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
        logger.error(
            f"Failed to download file to path {tmp_file_path}, of bucket {bucket_name} and file name {s3_file_name}: {e}")
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "File not found in S3"})
        }
    except Exception as e:
        logger.error(
            f"Something went wrong when downloading file to path {tmp_file_path}, of bucket {bucket_name} and file name {s3_file_name}: {e}")
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "File not found in S3"})
        }
    return tmp_file_path
