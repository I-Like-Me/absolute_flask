import time
import requests
import json
from authlib.jose import JsonWebSignature
from app import Config

class Abs_Actions:
    
    # Used for uploading Bitlocker data to device records.
    def abs_device_bitkey(deviceUid):
        token_id = Config.ABS_API_KEY
        token_secret = Config.ABS_API_SECRET
        request = {
            "method": "GET",
            "contentType": "application/json",
            "uri": f"/v3/configurations/customfields/devices/{deviceUid}/bpTvuBoVQfeWJYOfrDXlvQ",
            "queryString": "",
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
        return r, r_json
    
    # Used by Bokeh, Assets and Space Checker to track all hardware/OS data.
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
    
    # Used by Assets to track data from programs. [Cortext, InsightVM]
    def abs_all_apps(qust):
        token_id = Config.ABS_API_KEY
        token_secret = Config.ABS_API_SECRET
        request = {
            "method": "GET",
            "contentType": "application/json",
            "uri": "/v3/reporting/applications-advanced",
            "queryString": qust,
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
    
    # Used by Bokeh, CLI, and the Version Checker to track programs. [Citrix, Cortex, Zoom, InsightVM]
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

    