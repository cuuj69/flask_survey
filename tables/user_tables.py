import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Define the table name
table_name = 'UsersTable'  # Replace with your desired table name

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'  # String data type
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait for the table to be created before proceeding
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

print(f"Table '{table_name}' created successfully.")
