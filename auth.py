import datetime
import boto3

class Authentication:
    #session.user.userId
    @staticmethod
    def get_token(uid):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        response = table.get_item(
            Key={
                'uid': uid,
            }
        )
        item = response['Item']
        print(item)
        return item
    @staticmethod
    #    auth.post_token(d['name'], d['email'], d['user_id'])
    def post_token(name, email, uid):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        
        table.put_item(
            Item={
                    'name': name,
                    'email': email,
                    'uid': uid,
                    'following': [],
                }
        )
    #    auth.post_token(d['name'], d['email'], d['user_id'])
    @staticmethod
    def post_token(name, email, uid):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        
        table.put_item(
            Item={
                    'name': name,
                    'email': email,
                    'uid': uid,
                    'following': [],
                }
        )
    @staticmethod
    def delete_token(uid):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')

        table.delete_item(
            Key={
                'uid': uid
            }
        )
    @staticmethod
    def add_to_following(uid, followers):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        response = table.update_item(
            Key={
                'uid': uid
            },
            UpdateExpression="set user.following=:a",
            ExpressionAttributeValues={
                ':a': [followers]
            },
            ReturnValues="UPDATED_NEW"
        )

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='users',
        KeySchema=[
            {
                'AttributeName': 'uid',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uid',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.