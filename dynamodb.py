import boto3
from dotenv import load_dotenv
import os


load_dotenv

access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key =  os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

dynamodb = boto3.client('dynamodb',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)

