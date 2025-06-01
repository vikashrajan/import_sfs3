# lambda_snowflake_loader/lambda_function.py
import boto3
import snowflake.connector
import json
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f"Processing file: {key}")

    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')
    data = json.loads(file_content)

    conn = snowflake.connector.connect(
        user=os.environ['SF_USER'],
        password=os.environ['SF_PASSWORD'],
        account=os.environ['SF_ACCOUNT'],
        warehouse=os.environ['SF_WAREHOUSE'],
        database=os.environ['SF_DATABASE'],
        schema=os.environ['SF_SCHEMA']
    )

    cursor = conn.cursor()
    try:
        for record in data:
            cursor.execute("""
                INSERT INTO parsed_data (id, name, phone, address, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                record['id'], record['name'], record['phone'],
                record['address'], record['email']
            ))
    finally:
        cursor.close()
        conn.close()

    return {'statusCode': 200, 'body': f"Loaded {len(data)} records"}
