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
    
    def build_version_dict(app_choice, raw_data, version_data):
        version_dict = {}
        if app_choice.name == 'Citrix':
            for app in raw_data['data']:
                if 'Citrix Workspace' in app['appName'] or 'Citrix Receiver' in app['appName']:
                    for version in version_data:
                        if version.true_key == app['appVersion']:
                            version_dict[app['deviceName']] = [app['appName'], version.fake_key]
        if app_choice.name == 'Zoom':
            for app in raw_data['data']:
                if 'Zoom' in app['appName'] or 'Zoom(32bit)' in app['appName']:
                    for version in version_data:
                        if version.true_key == app['appVersion']:
                            version_dict[app['deviceName']] = [app['appName'], version.fake_key]
        if app_choice.name == 'Windows Product Level':
            for app in raw_data['data']:
                if 'build' in app['operatingSystem']:
                     for version in version_data:
                        if version.true_key == app['operatingSystem']['build']:
                            version_dict[app['deviceName']] = 'Windows', version.fake_key
        return version_dict
    
class Translators:

    def app_select_tlr(app_choice):
        if app_choice == 'Citrix':
            return "/v3/reporting/applications-advanced", "filter=(appNameContains eq 'receiver' or appNameContains eq 'workspace')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A"
        if app_choice == 'Zoom':
            return "/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Zoom')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A"
        if app_choice == 'Windows Product Level':
            return "/v3/reporting/devices", "pageSize=500&agentStatus=A"
        
class Table_List_Builder:
    
    def build_version_list(app_name, raw_data):
        unique_library_dict = {}
        if app_name == 'Citrix':
            for app in raw_data['data']:
                if 'Citrix Workspace' in app['appName']:
                    if app['appName'] not in unique_library_dict.keys() and app['appVersion'] not in unique_library_dict.values():
                        unique_library_dict[app['appName']] = app['appVersion']                    
                if 'Citrix Receiver' in app['appName']:
                    temp_receiver_name = f"{app['appName']}{app['appVersion']}"
                    if temp_receiver_name not in unique_library_dict.keys() and app['appVersion'] not in unique_library_dict.values():
                        unique_library_dict[temp_receiver_name] = app['appVersion']
        if app_name == 'Zoom':
            for app in raw_data['data']:
                if 'Zoom' in app['appName'] or 'Zoom(32bit)' in app['appName'] and app['appName'] not in unique_library_dict.keys() and app['appVersion'] not in unique_library_dict.values():
                    unique_library_dict[app['appName']] = app['appVersion']
        return unique_library_dict

class Library_Table_Dict_Builders:

    def ctx_lib_tab_dict(app_name, raw_data):
        unique_library_dict = {}
        if app_name == 'Citrix':
            for app in raw_data['data']:
                if 'Citrix Workspace' in app['appName'] or 'Citrix Receiver' in app['appName']:
                    correct_ver_name = VNM.citrix_name_maker(app['appVersion'])
                    if correct_ver_name not in unique_library_dict.keys() and app['appVersion'] not in unique_library_dict.values():
                        unique_library_dict[correct_ver_name] = app['appVersion']                    

        if app_name == 'Zoom':
            unique_library_dict = {}
            for app in raw_data['data']:
                if 'Zoom' in app['appName'] or 'Zoom(32bit)' in app['appName']:
                    correct_ver_name = VNM.zoom_name_maker(app['appVersion'])
                    if correct_ver_name not in unique_library_dict.values():
                        unique_library_dict[correct_ver_name] = app['appVersion']
        return unique_library_dict

class VNM: #Verison Name Maker

    def citrix_name_maker(old_ver):
        new_ver_name = ''
        fin_idx = 0
        sd = ['1','2','3','4','5','6','7','8','9']
        new_ver_name += old_ver[0:2]
        if old_ver[3] == '0' and old_ver[4] in sd or old_ver[3] in sd and old_ver[4] in sd or old_ver[3] in sd and old_ver[4] in '0':
            new_ver_name += old_ver[3:5]
            fin_idx = 6
        if old_ver[3] == 0 and old_ver[4] == '.':
            new_ver_name += '00'
            fin_idx = 5
        if old_ver[3] in sd and old_ver[4] == '.':
            new_ver_name += '0'
            new_ver_name += old_ver[3]
            fin_idx = 5
        new_ver_name += '.'    
        new_ver_name += old_ver[fin_idx:]
        return new_ver_name
    
    def zoom_name_maker(old_ver):
        old_ver = old_ver
        if ' ' in old_ver:
            old_ver = old_ver[:old_ver.index(' ')]
        new_ver_name = ''
        first_fin_idx = 0
        second_fin_idx = 0
        if old_ver.count('.') == 1:
            if old_ver[1] == '.':
                new_ver_name += '0'
                new_ver_name += old_ver[0:2]
                first_fin_idx = 2
            if old_ver[1] != '.':
                new_ver_name += old_ver[0:3]
                first_fin_idx = 3
            if old_ver[first_fin_idx-1] == '.' and old_ver[-2] == '.':
                new_ver_name += '0'
                new_ver_name += old_ver[-1]
            return new_ver_name      
        if old_ver.count('.') == 2:
            if old_ver[1] == '.':
                new_ver_name += '0'
                new_ver_name += old_ver[0:2]
                first_fin_idx = 2
            if old_ver[1] != '.':
                new_ver_name += old_ver[0:3]
                first_fin_idx = 3
            if old_ver[first_fin_idx-1] == '.' and old_ver[first_fin_idx +2] == '.':
                new_ver_name += old_ver[first_fin_idx:first_fin_idx+3]
                second_fin_idx += first_fin_idx+3
            if old_ver[first_fin_idx-1] == '.' and old_ver[first_fin_idx +2] != '.':
                new_ver_name += '0'
                new_ver_name += old_ver[first_fin_idx:first_fin_idx+2]
                second_fin_idx += first_fin_idx+2
            if old_ver[-2] == '.':
                new_ver_name += '0'
            new_ver_name += old_ver[second_fin_idx:]
            return new_ver_name