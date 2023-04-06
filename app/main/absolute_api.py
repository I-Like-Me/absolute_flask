import time
import requests
import json
from authlib.jose import JsonWebSignature
from app import Config, library

class Abs_Actions:

    def Abs_get(keyword_type_choice, keyword_choice):
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

    def prepare_data(raw_data):
        clean_data = {}
        clean_data['name'] = raw_data['data'][0]['deviceName']
        clean_data['manufacturer'] = raw_data['data'][0]['systemManufacturer']
        clean_data['model'] = raw_data['data'][0]['systemModel']
        clean_data['serial'] = raw_data['data'][0]['serialNumber']
        clean_data['ip'] = raw_data['data'][0]['localIp']
        for adapter in raw_data['data'][0]['networkAdapters']:
            if 'ipV4Address' in adapter and adapter['ipV4Address'] == clean_data['ip']:
                clean_data['mac'] = adapter['macAddress']
        clean_data['connected'] = raw_data['data'][0]['lastConnectedDateTimeUtc']
        clean_data['user'] = raw_data['data'][0]['currentUsername']
        clean_data['os'] = library.product_levels[raw_data['data'][0]['operatingSystem']['build']]
        for volume in raw_data['data'][0]['volumes']:
            if 'driveLetter' in volume and volume['driveLetter'] == 'C:':     
                clean_data['space'] = round(int(volume['freeSpaceBytes'])/(1024*1024*1024))
        clean_data['citrix'] = 'N/A'
        clean_data['cortex'] = 'N/A'
        clean_data['insight'] = 'N/A'
        clean_data['bitlocker'] = 'N/A'
        clean_data['member'] = 'N/A'
        return clean_data