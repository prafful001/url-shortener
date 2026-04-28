import boto3
import json
import string
import random
import os

# Connect to DynamoDB only when needed
def get_table():
    dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-south-1'))
    return dynamodb.Table('urls')

def generate_short_code():
    """Generate random 6 character code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def lambda_handler(event, context):
    method = event['httpMethod']
    
    # POST - Create short URL
    if method == 'POST':
        try:
            body = json.loads(event['body'])
            original_url = body['url']
            
            # Validate URL
            if not original_url.startswith('http'):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid URL'})
                }
            
            # Generate short code
            short_code = generate_short_code()
            
            # Save to DynamoDB
            get_table().put_item(Item={
                'short_code': short_code,
                'original_url': original_url
            })
            
            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'short_code': short_code,
                    'short_url': f"https://j4ilnschw7.execute-api.ap-south-1.amazonaws.com/prod/{short_code}",
                    'original_url': original_url
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    # GET - Redirect to original URL
    if method == 'GET':
        try:
            short_code = event['pathParameters']['code']
            
            # Fetch from DynamoDB
            response = get_table().get_item(
                Key={'short_code': short_code}
            )
            
            # 404 if not found
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'URL not found'})
                }
            
            # Redirect
            return {
                'statusCode': 301,
                'headers': {
                    'Location': response['Item']['original_url']
                },
                'body': ''
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }