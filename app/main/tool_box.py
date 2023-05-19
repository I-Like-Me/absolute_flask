from app import library

class Jsonizers:

    def space_json(key, value):
        return {
            'device': key,
            'size': value
        } 

    def version_json(key, value):
        return {
            'device':key,
            'app': value[0],
            'version': value[1]
        } 

class Dict_Builder:

    def build_space_dict(all_machines):
        space_dict = {}
        for machine in all_machines['data']:
            if 'volumes' in machine:
                for volume in machine['volumes']:
                    if 'driveLetter' in volume and volume['driveLetter'] == 'C:':
                        if round(int(volume['freeSpaceBytes'])/(1024*1024*1024)) <= 25:
                            space_dict[machine['deviceName']] = round(int(volume['freeSpaceBytes'])/(1024*1024*1024))
        return space_dict

    def build_machine_dict(raw_device_data, raw_app_data):
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
    
    def build_version_dict(app_choice, raw_data):
        version_dict = {}
        if app_choice == 'Citrix':
            for app in raw_data['data']:
                if 'Citrix Workspace' in app['appName'] or 'Citrix Receiver' in app['appName']:
                    version_dict[app['deviceName']] = [app['appName'], app['appVersion']]
        if app_choice == 'Zoom':
            for app in raw_data['data']:
                if 'Zoom' in app['appName'] or 'Zoom(32bit)' in app['appName']:
                    version_dict[app['deviceName']] = [app['appName'], app['appVersion']]
        if app_choice == 'Windows Product Level':
            for app in raw_data['data']:
                if 'build' in app['operatingSystem']:
                    version_dict[app['deviceName']] = ["Windows", library.product_levels[app['operatingSystem']['build']]]
        return version_dict
    
class Translators:

    def app_select_tlr(app_choice):
        if app_choice == 'Citrix':
            return "/v3/reporting/applications-advanced", "filter=(appNameContains eq 'receiver' or appNameContains eq 'workspace')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A"
        if app_choice == 'Zoom':
            return "/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Zoom')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A"
        if app_choice == 'Windows Product Level':
            return "/v3/reporting/devices", "pageSize=500&agentStatus=A"
        