import boto3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('UsersTable')

class User(UserMixin):
    def __init__(self,user_id,email,password_hash):
        self.id = user_id
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def generate_user_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def create(email,password):
        password_hash = generate_password_hash(password)
        user_id = User.generate_user_id()
        user_table.put_item(Item={'user_id':user_id, 'email':email, 'password_hash': password_hash})
    
    @staticmethod
    def get(user_id):
        response = user_table.get_item(Key={'user_id' : user_id})
        user_data = response.get('Item')
        if user_data:
            return User(user_id=user_data['user_id'], email=user_data['email'],password_hash=user_data['password_hash'])
        return None
    
    @staticmethod
    def get_by_email(email):
        response = user_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('email').eq(email))
        user_data = response.get('Items', [])
        if user_data:
            return User(user_id=user_data[0]['user_id'], email=user_data[0]['email'], password_hash=user_data[0]['password_hash'])
        return None
    

if __name__ == '__main__':
    pass