import time
import requests
import json
from authlib.jose import JsonWebSignature
from app import Config

class Abs_Actions:

    def abs_device_get(keyword_type_choice, keyword_choice):
        token_id = Config.ABS_API_KEY
        token_secret = Config.ABS_API_SECRET
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
        request_url = "https://api.absolute.com/jws/validate"
        r = requests.post(request_url, signed, {"content-type": "text/plain"})
        r_json = r.json()
        return r_json

    def abs_app_get(keyword_choice):
        token_id = Config.ABS_API_KEY
        token_secret = Config.ABS_API_SECRET
        request = {
            "method": "GET",
            "contentType": "application/json",
            "uri": "/v3/reporting/applications",
            "queryString": f"deviceName={keyword_choice}&select=appName,appVersion",
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
        request_url = "https://api.absolute.com/jws/validate"
        r = requests.post(request_url, signed, {"content-type": "text/plain"})
        r_json = r.json()
        return r_json
    
    def abs_all_devices(quSt):
        token_id = Config.ABS_API_KEY
        token_secret = Config.ABS_API_SECRET
        request = {
            "method": "GET",
            "contentType": "application/json",
            "uri": "/v3/reporting/devices",
            "queryString": quSt,
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
        request_url = "https://api.absolute.com/jws/validate"
        r = requests.post(request_url, signed, {"content-type": "text/plain"})
        r_json = r.json()
        return r_json

    def app_version_get(uri_picked, quSt):
        token_id = Config.ABS_API_KEY
        token_secret = Config.ABS_API_SECRET
        request = {
            "method": "GET",
            "contentType": "application/json",
            "uri": f"{uri_picked}",
            "queryString": f"{quSt}",
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
        request_url = "https://api.absolute.com/jws/validate"
        r = requests.post(request_url, signed, {"content-type": "text/plain"})
        r_json = r.json()
        return r_json
    