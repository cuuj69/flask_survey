import boto3
from dotenv import load_dotenv
import os


load_dotenv

access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key =  os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

dynamodb = boto3.client('dynamodb',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)

table_name ='SurveyAppTable'

try:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema= [
            {'AttributeName':'PK','KeyType':'HASH'},
            {'AttributeName':'SK','KeyType':'RANGE'},
        ],
        AttributeDefinitions=[
            {'AttributeName':'PK','AttributeType': 'S'},
            {'AttributeName':'SK','AttributeType':'S'}

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits':5,
            'WriteCapacityUnits':5
        }
    )
    print('Table created successfully!')
except Exception as e:
    print('Error creating table:', e)