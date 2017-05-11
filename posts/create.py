import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')
# s3 = boto3.resource('s3')


def create(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or 'title' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the post.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    # bucket = s3.Bucket(os.environ['S3_BUCKET'])

    header = upload(data['header'], bucket, 'header')
    screenshot = upload(data['screenshot'], bucket, 'screenshot')

    item = {
        'id': str(uuid.uuid1()),
        'title': data['title']
        'text': data['text'],
        'header': data['header'],
        'screenshot': data['screenshot'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response

# def upload(filename, bucket, type):
#     path = '/images/{}/{}'.format(type, filename)
#     s3.meta.client.upload_file(path, bucket, filename)
#     return filename
