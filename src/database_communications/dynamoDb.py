import logging
from datetime import datetime

import boto3

dynamodb = boto3.resource('dynamodb')
dynamoTableName = 'contract-status'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_to_dynamodb(id: str, result: str, status="completed"):
    logger.info(f"Uploading result for id: {id} with status: {status} to DynamoDB")
    table = dynamodb.Table(dynamoTableName)
    current_time = datetime.utcnow().isoformat()

    # Get current item
    response = table.get_item(Key={"contractId": id})
    existing_result = response.get("Item", {}).get("summary", "")

    # Append new content in Python
    combined_result = existing_result + result

    # Update item
    table.update_item(
        Key={"contractId": id},
        UpdateExpression="""
            SET summary = :combinedText,
                #contract_status = :status,
                updated_time = :updated
        """,
        ExpressionAttributeNames={
            "#contract_status": "status"
        },
        ExpressionAttributeValues={
            ":combinedText": combined_result,
            ":status": status,
            ":updated": current_time
        },
        ReturnValues="UPDATED_NEW"
    )
