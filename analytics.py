import http.client
import json
import time
import hashlib

def hash_any_identifier(input_string):
    input_string = str(input_string).encode('utf-8')
    hashed = hashlib.md5(input_string).hexdigest()
    short_hash = hashed[:5]
    return short_hash


def send_analytics_event(event_name, identifier):
    identifier = hash_any_identifier(identifier)
    conn = http.client.HTTPSConnection("api.mixpanel.com")
    payload = json.dumps([
    {
        "event": event_name,
        "properties": {
        "token": "e1a0475e9c22f81d247c3c5cc7e5813f",
        "time": int(time.time()),
        "distinct_id": identifier,
        }
    }
    ])
    headers = {
    'Accept': 'text/plain',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/track", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
