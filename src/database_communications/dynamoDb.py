from datetime import datetime

import boto3

dynamodb = boto3.resource('dynamodb')
dynamoTable = dynamodb.Table('contract-status')

def upload_to_dynamodb(id: str, result: str):
    dynamoTable.put_item(
        Item={
            'contractId': id,
            'status': 'completed',
            'result': result,
            'updatedAt': datetime.utcnow().isoformat(),
        }
    )