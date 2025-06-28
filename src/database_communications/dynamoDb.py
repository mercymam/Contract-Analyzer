import logging
from datetime import datetime

import boto3

dynamodb = boto3.resource('dynamodb')
dynamoTableName = 'contract-status'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_to_dynamodb(id: str, result: str, status = "completed"):
    logger.info(f"Uploading result for id: {id} with status: {status} to DynamoDB")
    current_time = datetime.utcnow().isoformat()
    dynamodb.update_item(
        TableName=dynamoTableName,
        Key={"file_id": {"S": id}},
        UpdateExpression="""
                SET result = if_not_exists(result, :empty) + :newText,
                    #contract_status = :status,
                    updated_time = :updated
            """,
        ExpressionAttributeNames={
            "#contract_status": "status"
        },
        ExpressionAttributeValues={
            ":newText": {"S": result},
            ":empty": {"S": ""},
            ":status": {"S": status},
            ":updated": {"S": current_time}
        },
        ReturnValues="UPDATED_NEW"
    )
