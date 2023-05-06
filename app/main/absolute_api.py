import time
import requests
import json
from authlib.jose import JsonWebSignature
from app import Config, library

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

    def graph_prep():
        graph_ready = {}
        all_results = Abs_Actions.abs_all_devices("pageSize=500&agentStatus=A")
        counter = 0
        for machine in all_results['data']:
            counter += 1
        graph_ready['total'] = counter
        counter = 0
        for machine in all_results['data']:
            if 'volumes' in machine:
                for volume in machine['volumes']:
                    if 'driveLetter' in volume and volume['driveLetter'] == 'C:':
                        if round(int(volume['freeSpaceBytes'])/(1024*1024*1024)) <= 25:
                            counter += 1
        graph_ready['less_then_25'] = counter        
        return graph_ready
        
        

    def prepare_data(raw_device_data, raw_app_data):
        clean_data = {}
        clean_data['name'] = raw_device_data['data'][0]['deviceName']
        clean_data['manufacturer'] = raw_device_data['data'][0]['systemManufacturer']
        clean_data['model'] = raw_device_data['data'][0]['systemModel']
        clean_data['serial'] = raw_device_data['data'][0]['serialNumber']
        clean_data['ip'] = raw_device_data['data'][0]['localIp']
        for adapter in raw_device_data['data'][0]['networkAdapters']:
            if 'ipV4Address' in adapter and adapter['ipV4Address'] == clean_data['ip']:
                clean_data['mac'] = adapter['macAddress']
        clean_data['connected'] = raw_device_data['data'][0]['lastConnectedDateTimeUtc']
        if 'currentUsername' in raw_device_data['data'][0]:
            clean_data['user'] = raw_device_data['data'][0]['currentUsername']
        if 'build' in raw_device_data['data'][0]['operatingSystem']:
            clean_data['os'] = library.product_levels[raw_device_data['data'][0]['operatingSystem']['build']]
        for volume in raw_device_data['data'][0]['volumes']:
            if 'driveLetter' in volume and volume['driveLetter'] == 'C:':     
                clean_data['space'] = round(int(volume['freeSpaceBytes'])/(1024*1024*1024))
        for app in raw_app_data['data']:
            if 'Citrix Workspace' in app['appName'] or 'Citrix Receiver' in app['appName']:
                clean_data['citrix'] = app['appName']
        clean_data['cortex'] = 'No'
        for app in raw_app_data['data']:
            if 'Cortex' in app['appName']:    
                clean_data['cortex'] = 'Yes'
        clean_data['insight'] = 'No'
        for app in raw_app_data['data']:
            if 'Rapid7' in app['appName']: 
                clean_data['insight'] = 'Yes'
        clean_data['bitlocker'] = 'N/A'
        clean_data['member'] = 'N/A'
        return clean_data
    
    def build_space_list(all_machines):
        space_dict = {}
        for machine in all_machines['data']:
            if 'volumes' in machine:
                for volume in machine['volumes']:
                    if 'driveLetter' in volume and volume['driveLetter'] == 'C:':
                        if round(int(volume['freeSpaceBytes'])/(1024*1024*1024)) <= 25:
                            space_dict[machine['deviceName']] = round(int(volume['freeSpaceBytes'])/(1024*1024*1024))
        return space_dict
