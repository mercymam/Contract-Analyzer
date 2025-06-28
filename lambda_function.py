import json
import logging
import boto3
import asyncio

from src.database_communications.s3 import download_file_path_from_s3
from src.file_processing.extract_file_details import process_pdf_text_in_batches
from urllib.parse import unquote

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DYNAMODB_TABLE = 'contract-status'
RESULT_BUCKET = 'contract-analyzer-bucket'

dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    logger.info(f"Event received: {json.dumps(event)}")
    if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:s3':
        asyncio.run(handle_s3_trigger(event))
    elif event.get('contractId'):
        return handle_api_trigger(event)
    elif event.get('filename'):
        return generate_presigned_url(event)
    else: return{
        'statusCode': 400,
        'body': json.dumps({'error': 'Unsupported event type'})
    }

def handle_api_trigger(event):
    contract_id = unquote(event.get('contractId'))
    logger.info(f"Successfully retrieved Contract ID: {contract_id}")
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
        result_text = item.get('summary', '')
        logger.info(f"Result text: {result_text}")
        return result_text

    except Exception as e:
        logger.error("DynamoDB retrieval failed", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


async def handle_s3_trigger(event):
        try:
            tmp_file_path, file_identifier = download_file_path_from_s3(event)
            ai_response = await process_pdf_text_in_batches(tmp_file_path, file_identifier)
            logger.info(f"Summarised text for file Id: {file_identifier} (first 200 chars): {ai_response[:200]}")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Tenancy contract analyzed successfully",
                    "result_key": file_identifier,
                    "excerpt": ai_response[:500]
                })
            }

        except Exception as e:
            logger.error("Unhandled exception", exc_info=True)
            return {
                "statusCode": 500,
                "body": json.dumps({"Exception occurred": str(e)})
            }


def generate_presigned_url(event):
    try:
        filename = unquote(event.get('filename'))

        if not filename:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "filename"'})
            }

        s3_client = boto3.client('s3')
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': RESULT_BUCKET,
                'Key': f'{filename}',
                'ContentType': 'application/pdf'
            },
            ExpiresIn=3000  # 5 minutes
        )

        return presigned_url

    except Exception as e:
        logger.error("Error generating pre-signed URL", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

