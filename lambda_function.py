import asyncio
import json
import logging

import boto3

from src.data_processing.truncator import truncate_to_fit
from src.database_communications.dynamoDb import upload_to_dynamodb
from src.database_communications.s3 import download_file_path_from_s3
from src.file_processing.extract_file_details import extract_pdf_text, extract_uuid_from_filename
from src.data_processing.llm import call_llm_api
from src.prompt.prompt import tenancy_analysis_prompt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DYNAMODB_TABLE = 'contract-status'
RESULT_BUCKET = 'contract-analyzer-bucket'
RESULT_PREFIX = 'result'

dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    logger.info(f"Event received: {json.dumps(event)}")
    if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:database_communications':
        handle_s3_trigger(event)
    elif event.get('httpMethod') == 'GET' and event.get('pathParameters'):
        handle_api_trigger(event, context)
    else: return{
        'statusCode': 400,
        'body': json.dumps({'error': 'Unsupported event type'})
    }

def handle_api_trigger(event):
    contract_id = event['pathParameters'].get('contractId')

    if not contract_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing contractId'})
        }

    try:
        response = dynamo_table.get_item(Key={'contractId': contract_id})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Contract not found'})
            }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(item)
        }

    except Exception as e:
        logger.error("DynamoDB retrieval failed", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def handle_s3_trigger(event):
    try:
        tmp_file_path = download_file_path_from_s3(event)
        extracted_text = asyncio.run(extract_pdf_text(tmp_file_path))
        logger.info(f"Extracted text (first 200 chars): {extracted_text[:200]}")

        truncated_texts = truncate_to_fit(tenancy_analysis_prompt, extracted_text, "gpt-3.5-turbo", "openai")
        ai_response = ""
        for i, text in enumerate(truncated_texts):
            logger.info(f"Calling LLM for chunk {i}")
            response = call_llm_api(tenancy_analysis_prompt, text)
            if response:
                ai_response += response

        file_identifier = extract_uuid_from_filename(tmp_file_path)
        if ai_response:
            upload_to_dynamodb(file_identifier, ai_response)
            logger.info(f"Uploaded AI response to dynamo_db at {file_identifier}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Tenancy contract analyzed successfully",
                "result_key": file_identifier,
                "excerpt": ai_response[:500]
            })
        }

    except Exception as e:
        logger.error(f"Unhandled exception", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"Exception occurred": str(e)})
        }




