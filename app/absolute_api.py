import time
import requests
import json
from authlib.jose import JsonWebSignature
from app import Config

class Abs_Actions:

    def Abs_get(keyword_type_choice, keyword_choice):
        # Fill in the Token ID for your API token
        token_id = Config.ABS_API_KEY
        # Fill in the Secret Key for your API token
        token_secret = Config.ABS_API_SECRET
        # Build the request
        request = {
            "method": "GET",
            "contentType": "application/json",
            "uri": "/v3/reporting/devices",
            "queryString": f"{keyword_type_choice}={keyword_choice}",
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
        request_url = "https://api.absolute.com/jws/validate"
        r = requests.post(request_url, signed, {"content-type": "text/plain"})
        r_json = r.json()
        #print(r.content)
        #device_name = r_json["data"][0]["deviceName"]
        #user_name = r_json["data"][0]["userName"]
        #if r_json['data'] == []:
            #print('True')
        return r_json
        #print(r_json['data'])