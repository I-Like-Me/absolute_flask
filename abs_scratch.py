import time
import requests
import json
from authlib.jose import JsonWebSignature
from config import Config

# Fill in the Token ID for your API token
token_id = Config.ABS_API_KEY
# Fill in the Secret Key for your API token
token_secret = Config.ABS_API_SECRET
# Build the request
request = {
    "method": "GET",
    "contentType": "application/json",
    "uri": "/v3/reporting/applications",
    "queryString": "select=appName",
    "payload": {}
}
request_payload_data = {
    "data": request["payload"]
}
headers = {
    "alg": "HS256",
    "kid": token_id,
    "method": request["method"],
    "content-type": request["contentType"],
    "uri": request["uri"],
    "query-string": request["queryString"],
    "issuedAt": round(time.time() * 1000)
}


jws = JsonWebSignature()
signed = jws.serialize_compact(headers, json.dumps(request_payload_data), token_secret)


# Make the actual request
# Update the request_url, if required:
# If you log in to https://cc.absolute.com,
# use https://api.absolute.com/jws/validate.
# If you log in to https://cc.us.absolute.com,
# use https://api.us.absolute.com/jws/validate.
# If you log in to https://cc.eu2.absolute.com,
# use https://api.eu2.absolute.com/jws/validate.
request_url = "https://api.absolute.com/jws/validate"
r = requests.post(request_url, signed, {"content-type": "text/plain"})
print(r.content)