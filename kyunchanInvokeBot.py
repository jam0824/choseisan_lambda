import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logging.info(json.dumps(event))

    
    if "challenge" in event:
        return event.get("challenge")
    
    if "X-Slack-Retry-Num" not in event["headers"]:
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName='kyunchan',
            InvocationType='Event',
            LogType='Tail',
            Payload= json.dumps(event)
        )

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }