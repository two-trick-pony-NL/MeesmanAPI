import http.client
import json
import boto3


url = "https://exp.host/--/api/v2/push/send"


def send_push_message(token, message_title, message_body):
    conn = http.client.HTTPSConnection("exp.host")
    payload = json.dumps({
        "to": token,
        "title": message_title,
        "body": message_body
        })
    headers = {
        'Content-Type': 'application/json'
        }
    conn.request("POST", "/--/api/v2/push/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    if res.status == 200:
        return True
    else:
        return False


def save_to_dynamodb(string_data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MeesmanPushTokens')
    # Assuming 'id' is the sort key
    table.put_item(Item={'id': string_data})

def get_all_strings_from_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MeesmanPushTokens')

    response = table.scan()
    # Assuming 'id' is the sort key
    all_strings = [item['id'] for item in response.get('Items', [])]
    return all_strings


 
