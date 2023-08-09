from app import library
from datetime import datetime 
import pandas as pd

class Jsonizers:

    def space_json(key, value):
        return {
            'device': key,
            'size': value
        }

    def request_json(key, value):
        return {
            'device': key,
            'user': value[0],
            'manufacturer': value[1],
            'model': value[2],
            'serial': value[3],
            'ip': value[4],
            'mac': value[5],
            'connected': value[6],
            'os': value[7],
            'space': value[8]
        }  

    def version_json(key, value):
        return {
            'device':key,
            'app': value[0],
            'version': value[1]
        } 

class Dict_Builder:

    def build_request_dict(all_machines):
        request_dict = {}
        for machine in all_machines['data']: 
            if 'currentUsername' in machine:
                request_dict[machine['deviceName']] = [machine['currentUsername']]
            else:
                request_dict[machine['deviceName']] = ['N/A']    
            if 'systemManufacturer' in machine:
                request_dict[machine['deviceName']].append(machine['systemManufacturer'])
            else:
                request_dict[machine['deviceName']].append('N/A')
            if 'systemModel' in machine:
                request_dict[machine['deviceName']].append(machine['systemModel'])
            else:
                request_dict[machine['deviceName']].append('N/A')
            if 'serialNumber' in machine:
                request_dict[machine['deviceName']].append(machine['serialNumber'])
            else:
                request_dict[machine['deviceName']].append('N/A')
            if 'localIp' in machine:
                request_dict[machine['deviceName']].append(machine['localIp'])
            else:
                request_dict[machine['deviceName']].append('N/A')
            if 'networkAdapters' in machine:
                for adapter in machine['networkAdapters']:
                    if 'ipV4Address' in adapter and 'macAddress' in adapter and adapter['ipV4Address'] == request_dict[machine['deviceName']][4]:
                        request_dict[machine['deviceName']].append(adapter['macAddress'])
                    if 'ipV4Address' in adapter and adapter['manufacturer'] == 'Cisco Systems' and adapter['ipV4Address'] == request_dict[machine['deviceName']][4]:
                        request_dict[machine['deviceName']].append('Last connected through VPN.')
                if len(request_dict[machine['deviceName']]) == 5:
                    request_dict[machine['deviceName']].append('N/A') 
            else:
                request_dict[machine['deviceName']].append('N/A')  
            if 'lastConnectedDateTimeUtc' in machine:
                request_dict[machine['deviceName']].append(machine['lastConnectedDateTimeUtc'][:10])
            else:
                request_dict[machine['deviceName']].append('N/A')
            if 'build' in machine['operatingSystem']:
                request_dict[machine['deviceName']].append(library.product_levels[machine['operatingSystem']['build']])
            else:
                request_dict[machine['deviceName']].append('N/A')
            if 'volumes' in machine:
                for volume in machine['volumes']:
                    if 'driveLetter' in volume and volume['driveLetter'] == 'C:':
                        request_dict[machine['deviceName']].append(f"{str(round(int(volume['freeSpaceBytes'])/(1024*1024*1024)))} GB")
                if len(request_dict[machine['deviceName']]) == 9:
                    request_dict[machine['deviceName']].append('N/A') 
            else:
                request_dict[machine['deviceName']].append('N/A')
        return request_dict

    def build_space_dict(all_machines):
        space_dict = {}
        for machine in all_machines['data']:
            if 'volumes' in machine:
                for volume in machine['volumes']:
                    if 'driveLetter' in volume and volume['driveLetter'] == 'C:':
                        if round(int(volume['freeSpaceBytes'])/(1024*1024*1024)) <= 25:
                            space_dict[machine['deviceName']] = round(int(volume['freeSpaceBytes'])/(1024*1024*1024))
        return space_dict

    def build_machine_dict(raw_device_data, raw_app_data, raw_bit_data):
        clean_data = {}
        clean_data['name'] = raw_device_data['data'][0]['deviceName']
        clean_data['manufacturer'] = raw_device_data['data'][0]['systemManufacturer']
        clean_data['model'] = raw_device_data['data'][0]['systemModel']
        clean_data['serial'] = raw_device_data['data'][0]['serialNumber']
        clean_data['ip'] = raw_device_data['data'][0]['localIp']
        for adapter in raw_device_data['data'][0]['networkAdapters']:
            if 'ipV4Address' in adapter and 'macAddress' in adapter and adapter['ipV4Address'] == clean_data['ip']:
                clean_data['mac'] = adapter['macAddress']
            if 'ipV4Address' in adapter and adapter['manufacturer'] == 'Cisco Systems' and adapter['ipV4Address'] == clean_data['ip']:
                clean_data['mac'] = 'Last connected through VPN.'
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
        if str(raw_bit_data[0]) == '<Response [200]>':
            clean_data['bitlocker'] = raw_bit_data[1]['data']['cdfFieldValue']
        if str(raw_bit_data[0]) != '<Response [200]>':
            clean_data['bitlocker'] = 'no entry'
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
    
    def dict_for_df(dept_dicts):
        all_depts_data = {
            "dept_names": [],
            "space_counts": [],
            "dept_counts": [],
            "bit_counts": [],
            "ctx_ver_counts": [],
            "zm_ver_counts": [],
            "wpl_ver_counts": [],
            "cor_counts": [],
            "ivm_counts": [],
            "dell_counts": [],
            "lenovo_counts": [],
            "vul_counts": [],
            "exp_counts": [],
            "mal_counts": [],
            "year_1_counts": [],
            "year_2_counts": [],
            "year_3_counts": [],
            "year_4_counts": [],
            "year_5_counts": [],
            "dept_group_tag": [],
            "filter_lp": [],
            "filter_bk": [],
            "filter_second_floor": [],
            "filter_third_floor": [],
            "filter_fourth_floor": [],
            "filter_726": [],
            "filter_all": [],
        }
        
        for dept in dept_dicts:
            all_depts_data['dept_names'].append(dept)
            all_depts_data['space_counts'].append(dept_dicts[dept]['space_count'])
            all_depts_data['dept_counts'].append(dept_dicts[dept]['dept_count'])
            all_depts_data['bit_counts'].append(dept_dicts[dept]['bit_count'])
            all_depts_data['ctx_ver_counts'].append(dept_dicts[dept]['ctx_ver_count'])
            all_depts_data['zm_ver_counts'].append(dept_dicts[dept]['zm_ver_count'])
            all_depts_data['wpl_ver_counts'].append(dept_dicts[dept]['wpl_ver_count'])
            all_depts_data['cor_counts'].append(dept_dicts[dept]['cor_count'])
            all_depts_data['ivm_counts'].append(dept_dicts[dept]['ivm_count'])
            all_depts_data['dell_counts'].append(dept_dicts[dept]['dell_count'])
            all_depts_data['lenovo_counts'].append(dept_dicts[dept]['lenovo_count'])
            all_depts_data['vul_counts'].append(dept_dicts[dept]['vul_count'])
            all_depts_data['exp_counts'].append(dept_dicts[dept]['exp_count'])
            all_depts_data['mal_counts'].append(dept_dicts[dept]['mal_count'])
            all_depts_data['year_1_counts'].append(dept_dicts[dept]['year_1_count'])
            all_depts_data['year_2_counts'].append(dept_dicts[dept]['year_2_count'])
            all_depts_data['year_3_counts'].append(dept_dicts[dept]['year_3_count'])
            all_depts_data['year_4_counts'].append(dept_dicts[dept]['year_4_count'])
            all_depts_data['year_5_counts'].append(dept_dicts[dept]['year_5_count'])
            all_depts_data["dept_group_tag"].append(Data_fillers.dept_group_tagger(dept))
            all_depts_data["filter_lp"].append(Data_fillers.filter_laptops_tagger(dept))
            all_depts_data["filter_bk"].append(Data_fillers.filter_brooklyn_tagger(dept))
            all_depts_data["filter_726"].append(Data_fillers.filter_726_tagger(dept))
            all_depts_data["filter_second_floor"].append(Data_fillers.filter_2_floor_tagger(dept))
            all_depts_data["filter_third_floor"].append(Data_fillers.filter_3_floor_tagger(dept))
            all_depts_data["filter_fourth_floor"].append(Data_fillers.filter_4_floor_tagger(dept))
            all_depts_data["filter_all"].append('yes')
        return all_depts_data

class Translators:

    def app_select_tlr(app_choice):
        if app_choice == 'Citrix':
            return "/v3/reporting/applications-advanced", "filter=(appNameContains eq 'receiver' or appNameContains eq 'workspace')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A"
        if app_choice == 'Zoom':
            return "/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Zoom')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A"
        if app_choice == 'Windows Product Level':
            return "/v3/reporting/devices", "pageSize=500&agentStatus=A"
        
    def opt_select_tlr(operator, ver_choice, ver_dict):
        filtered_dict = {}
        for ver_key, ver_val in ver_dict.items():
            if operator == "is" and ver_val[1] == ver_choice.fake_key:
                filtered_dict[ver_key] = ver_val
            if operator == "not" and ver_val[1] != ver_choice.fake_key:
                filtered_dict[ver_key] = ver_val
            if operator == "less than" and ver_val[1] < ver_choice.fake_key:
                filtered_dict[ver_key] = ver_val
            if operator == "greater than" and ver_val[1] > ver_choice.fake_key:
                filtered_dict[ver_key] = ver_val
            if operator == "is or less than" and ver_val[1] <= ver_choice.fake_key:
                filtered_dict[ver_key] = ver_val
            if operator == "is or greater than" and ver_val[1] >= ver_choice.fake_key:
                filtered_dict[ver_key] = ver_val
        return filtered_dict
    
    def get_age(year_made):
        int_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if year_made[-1] in int_list and year_made[-2] in int_list:
            return int(datetime.today().year) - int('20' + year_made[-2:])
        else:
            return None
    
    def get_ip(curr_device, raw_device_data):
        for device in raw_device_data['data']:
            if device['deviceName'] == curr_device:
                return device['localIp']

    def get_manufacturer(curr_device, raw_device_data):
        for device in raw_device_data['data']:
            if device['deviceName'] == curr_device:
                return device['systemManufacturer']

    def get_space(curr_device, raw_device_data):
        for device in raw_device_data['data']:
            if device['deviceName'] == curr_device:
                if 'volumes' in device:
                    for volume in device['volumes']:
                        if 'driveLetter' in volume and volume['driveLetter'] == 'C:':     
                            return round(int(volume['freeSpaceBytes'])/(1024*1024*1024))
    
    def get_ncr(curr_device, raw_device_data):
        for device in raw_device_data['data']:
            if device['deviceName'] == curr_device:
                if 'espInfo' in device:
                    if device['espInfo']['encryptionStatus'] == 'USENCR':
                        return True
                    if device['espInfo']['encryptionStatus'] == 'ENCR':
                        return True
                    if device['espInfo']['encryptionStatus'] == 'SUSP':
                        return True
                    if device['espInfo']['encryptionStatus'] == 'UNKN':
                        return True
                    if device['espInfo']['encryptionStatus'] == 'INST':
                        return False

    def get_os_build(curr_device, raw_device_data):
        for device in raw_device_data['data']:
            if device['deviceName'] == curr_device:
                if 'build' in device['operatingSystem']:
                    return library.product_levels[device['operatingSystem']['build']]
            
    def get_citrix_ver(curr_device, raw_data):
        for app in raw_data['data']:
            if app['deviceName'] == curr_device:
                if 'Citrix Workspace' in app['appName'] or 'Citrix Receiver' in app['appName']:
                    correct_ver_name = VNM.citrix_name_maker(app['appVersion'])
                    return correct_ver_name
    
    def get_zoom_ver(curr_device, raw_data):
        for app in raw_data['data']:
            if app['deviceName'] == curr_device:
                if 'Zoom' in app['appName'] or 'Zoom(32bit)' in app['appName']:
                    correct_ver_name = VNM.zoom_name_maker(app['appVersion'])
                    return correct_ver_name
    
    def get_cortex(curr_device, raw_data):
        device_list = []
        for device in raw_data['data']:
            device_list.append(device['deviceName'])
        if curr_device in device_list:
            return True
        else:
            return False

    def get_insightvm(curr_device, raw_data):
        device_list = []
        for device in raw_data['data']:
            device_list.append(device['deviceName'])
        if curr_device in device_list:
            return True
        else:
            return False
        
    def get_dept(device_name, device_subnet):
        dept_global = ["FLORANCE", "CSLA", "BUENOS", "BERLIN", "PRAGUE"]
        dept_offsite = ["128.122.101", "216.165.95", "128.122.111", "128.122.132", "128.122.226"]
        dept_lp = {
            "AD_LP_Viz_Data": 2, 
            "AI_LP_Viz_Data": 2, 
            "CS_LP_Viz_Data": 2, 
            "FAC_LP_Viz_Data": 3, 
            "FI_LP_Viz_Data": 2, 
            "HPO_LP_Viz_Data": 3, 
            "IF_LP_Viz_Data": 2, 
            "IT_LP_Viz_Data": 2, 
            "LW_LP_Viz_Data": 2, 
            "MC_LP_Viz_Data": 2, 
            "MR_LP_Viz_Data": 2, 
            "NH_LP_Viz_Data": 2, 
            "OPTO_LP_Viz_Data": 2, 
            "PA_LP_Viz_Data": 2, 
            "PC_LP_Viz_Data": 2, 
            "PHA_LP_Viz_Data": 3, 
            "POPUP_Viz_Data": 3, 
            "PSS_LP_Viz_Data": 3, 
            "PT_LP_Viz_Data": 2, 
            "SP_LP_Viz_Data": 2, 
            "WH_LP_Viz_Data": 2, 
            "WL_LP_Viz_Data": 2
            }
        dept_subnets = {
            "AD_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "AI_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "COMF2_Viz_Data": [5, "192.168.7"],
            "COMF3_Viz_Data": [5, "128.122.56", "128.122.57", "172.22.56", "172.22.57"],
            "COMF4_Viz_Data": [5, "128.122.56", "128.122.57", "172.22.56", "172.22.57"],
            "COMF_BK_Viz_Data": [4, "128.122.33", "172.22.33"],
            "CS3_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "CS4_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "CS_BK_Viz_Data": [2, "128.122.33", "172.22.33"], 
            "FAC_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "FI_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "HPO_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"],  
            "IF_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "IT_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "KIT_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "LW_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "MC2_Viz_Data": [3, "192.168.7"], 
            "MC3_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "MC_BK_Viz_Data": [2, "128.122.33", "172.22.33"], 
            "MR_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "NH_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "OPTO_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "PA_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"],  
            "PC3_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "PC4_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "PC_BK_Viz_Data": [2, "128.122.33", "172.22.33"], 
            "PHA_Viz_Data": [3, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "PT_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "SP_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "WH_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"], 
            "WL_Viz_Data": [2, "128.122.56", "128.122.57", "172.22.56", "172.22.57"]
            }
        
        for place in dept_global:
            if place in device_name:
                return "GLOBAL_Viz_Data"
        if device_subnet[:10] in dept_offsite:
            return "OFF_Viz_Data"
        if device_subnet[:11] in dept_offsite:
            return "OFF_Viz_Data"
        for dept in dept_subnets:
            if device_name[:dept_subnets[dept][0]] == dept[:dept_subnets[dept][0]] and device_subnet[:9] in dept_subnets[dept]:
                return dept
            if device_name[:dept_subnets[dept][0]] == dept[:dept_subnets[dept][0]] and device_subnet[:10] in dept_subnets[dept]:
                return dept
        for dept in dept_lp:
            if device_name[:dept_lp[dept]] == dept[:dept_lp[dept]]:
                return dept

class List_builders:

    def full_device_name_list(raw_abs_data):
        device_name_list = []
        for device in raw_abs_data['data']:
            device_name_list.append(device["deviceName"])
        return device_name_list

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

class BDT: #Blank Dict Template
    
    def blank_graph_dict(graph_dict_name):
        graph_dict_name = {
            "space_count": 0,
            "dept_count": 0,
            "bit_count": 0,
            "ctx_ver_count": 0,
            "zm_ver_count": 0,
            "wpl_ver_count": 0,
            "cor_count": 0,
            "ivm_count": 0,
            "dell_count": 0,
            "lenovo_count": 0,
            "vul_count": 0,
            "exp_count": 0,
            "mal_count": 0,
            "year_1_count": 0,
            "year_2_count": 0,
            "year_3_count": 0,
            "year_4_count": 0,
            "year_5_count": 0
        }
        return graph_dict_name
    
    def blank_device_dict(device_dict_name):
        device_dict_name = {
            "dept": '', 
            "space": '',
            "ncr_status": '',
            "ip": '',
            "ctx_ver": '',
            "zm_ver": '',
            "wpl_ver": '',
            "cor": False,
            "ivm": False,
            "manufacturer": '',
            "vul_count": 0,
            "exp_count": 0,
            "mal_count": 0,
            "age": ''
        }
        return device_dict_name
    
    def blank_unique_ver_dict(dept_dict_names):
        dept_dict_names = {
            'citrix': [],
            'zoom': [],
            'build': []
        }
        return dept_dict_names
    
class MDG: #Multi Dict Generator
    
    def build_graph_series():
        series_keys = ["AD_Viz_Data", "AD_LP_Viz_Data", "AI_Viz_Data", "AI_LP_Viz_Data", 
                       "CONF2_Viz_Data", "CONF3_Viz_Data", "CONF4_Viz_Data", "CONF_BK_Viz_Data", 
                       "CS3_Viz_Data", "CS4_Viz_Data", "CS_BK_Viz_Data", "CS_LP_Viz_Data", 
                       "FAC_Viz_Data", "FAC_LP_Viz_Data", "FI_Viz_Data", "FI_LP_Viz_Data", 
                       "GLOBAL_Viz_Data", "HPO_Viz_Data", "HPO_LP_Viz_Data", "IF_Viz_Data", 
                       "IF_LP_Viz_Data", "IT_Viz_Data", "IT_LP_Viz_Data", "KIT_Viz_Data", 
                       "LW_Viz_Data", "LW_LP_Viz_Data", "MC2_Viz_Data", "MC3_Viz_Data", 
                       "MC_BK_Viz_Data", "MC_LP_Viz_Data", "MR_Viz_Data", "MR_LP_Viz_Data", 
                       "NH_Viz_Data", "NH_LP_Viz_Data", "OFF_Viz_Data", "OPTO_Viz_Data", 
                       "OPTO_LP_Viz_Data", "PA_Viz_Data", "PA_LP_Viz_Data", "PC3_Viz_Data", 
                       "PC4_Viz_Data", "PC_BK_Viz_Data", "PC_LP_Viz_Data", "PHA_Viz_Data", 
                       "PHA_LP_Viz_Data", "POPUP_Viz_Data", "PSS_LP_Viz_Data", "PT_Viz_Data", 
                       "PT_LP_Viz_Data", "SP_Viz_Data", "SP_LP_Viz_Data", "WH_Viz_Data", 
                       "WH_LP_Viz_Data", "WL_Viz_Data", "WL_LP_Viz_Data"]
        graph_series = {}
        for key in series_keys:
            graph_series[key] = BDT.blank_graph_dict(key)
        return graph_series
    
    def build_device_series(device_name_list):
        device_names = device_name_list
        device_series = {}
        for name in device_names:
            device_series[name] = BDT.blank_device_dict(name)
        return device_series
    
    def build_unique_ver_tracker():
        dept_list = ["AD_Viz_Data", "AD_LP_Viz_Data", "AI_Viz_Data", "AI_LP_Viz_Data", 
                     "CONF_Viz_Data", "CS3_Viz_Data", "CS4_Viz_Data", "CS_BK_Viz_Data", 
                     "CS_LP_Viz_Data", "FAC_Viz_Data", "FAC_LP_Viz_Data", "FI_Viz_Data", 
                     "FI_LP_Viz_Data", "GLOBAL_Viz_Data", "HPO_Viz_Data", "HPO_LP_Viz_Data", 
                     "IF_Viz_Data", "IF_LP_Viz_Data", "IT_Viz_Data", "IT_LP_Viz_Data", 
                     "KIT_Viz_Data", "LW_Viz_Data", "LW_LP_Viz_Data", "MC2_Viz_Data", 
                     "MC3_Viz_Data", "MC_BK_Viz_Data", "MC_LP_Viz_Data", "MR_Viz_Data", 
                     "MR_LP_Viz_Data", "NH_Viz_Data", "NH_LP_Viz_Data", "OFF_Viz_Data", 
                     "OPTO_Viz_Data", "OPTO_LP_Viz_Data", "PA_Viz_Data", "PA_LP_Viz_Data", 
                     "PC3_Viz_Data", "PC4_Viz_Data", "PC_BK_Viz_Data", "PC_LP_Viz_Data", 
                     "PHA_Viz_Data", "PHA_LP_Viz_Data", "POPUP_Viz_Data", "PSS_LP_Viz_Data", 
                     "PT_Viz_Data", "PT_LP_Viz_Data", "SP_Viz_Data", "SP_LP_Viz_Data", 
                     "WH_Viz_Data", "WH_LP_Viz_Data", "WL_Viz_Data", "WL_LP_Viz_Data"]
        version_tracker = {}
        for dept in dept_list:
            version_tracker[dept] = BDT.blank_unique_ver_dict(dept)
        return version_tracker

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
        
class Data_fillers:

    def fill_device_series(device_data, citrix_data, zoom_data, cortex_data, ivm_data):
        series = MDG.build_device_series(List_builders.full_device_name_list(device_data))
        for device in series:
            series[device]['age'] = Translators.get_age(device)
            series[device]['ip'] = Translators.get_ip(device, device_data)
            series[device]['dept'] = Translators.get_dept(device, series[device]['ip'])
            series[device]['space'] = Translators.get_space(device, device_data)
            series[device]['manufacturer'] = Translators.get_manufacturer(device, device_data)
            series[device]['ncr_status'] = Translators.get_ncr(device, device_data)
            series[device]['wpl_ver'] = Translators.get_os_build(device, device_data)
            series[device]['ctx_ver'] = Translators.get_citrix_ver(device, citrix_data)
            series[device]['zm_ver'] = Translators.get_zoom_ver(device, zoom_data)
            series[device]['cor'] = Translators.get_cortex(device, cortex_data)
            series[device]['ivm'] = Translators.get_insightvm(device, ivm_data)
        return series
    
    def fill_dept_series(device_dicts):
        total_device_count = 0
        version_tracker = MDG.build_unique_ver_tracker()
        dict_series = MDG.build_graph_series()
        for device in device_dicts:
            total_device_count += 1
            if device_dicts[device]['dept'] != None:
                dict_series[device_dicts[device]['dept']]['dept_count'] += 1
                if device_dicts[device]['space'] != None:
                    if int(device_dicts[device]['space']) <= 25:
                        dict_series[device_dicts[device]['dept']]['space_count'] += 1
                if device_dicts[device]['age'] != None:
                    if device_dicts[device]['age'] <= 1:
                        dict_series[device_dicts[device]['dept']]['year_1_count'] += 1
                    if device_dicts[device]['age'] == 2:
                        dict_series[device_dicts[device]['dept']]['year_2_count'] += 1
                    if device_dicts[device]['age'] == 3:
                        dict_series[device_dicts[device]['dept']]['year_3_count'] += 1
                    if device_dicts[device]['age'] == 4:
                        dict_series[device_dicts[device]['dept']]['year_4_count'] += 1
                    if device_dicts[device]['age'] >= 5:
                        dict_series[device_dicts[device]['dept']]['year_5_count'] += 1
                if device_dicts[device]['ncr_status'] != None:
                    if device_dicts[device]['ncr_status'] == True:
                        dict_series[device_dicts[device]['dept']]['bit_count'] += 1
                if device_dicts[device]['cor'] != None:
                    if device_dicts[device]['cor'] == True:
                        dict_series[device_dicts[device]['dept']]['cor_count'] += 1
                if device_dicts[device]['ivm'] != None:
                    if device_dicts[device]['ivm'] == True:
                        dict_series[device_dicts[device]['dept']]['ivm_count'] += 1
                if device_dicts[device]['manufacturer'] != None:
                    if device_dicts[device]['manufacturer'] == 'Dell':
                        dict_series[device_dicts[device]['dept']]['dell_count'] += 1
                if device_dicts[device]['manufacturer'] != None:
                    if device_dicts[device]['manufacturer'] == 'Lenovo':
                        dict_series[device_dicts[device]['dept']]['lenovo_count'] += 1 
                dict_series[device_dicts[device]['dept']]['vul_count'] += device_dicts[device]['vul_count']
                dict_series[device_dicts[device]['dept']]['exp_count'] += device_dicts[device]['exp_count']
                dict_series[device_dicts[device]['dept']]['mal_count'] += device_dicts[device]['mal_count']
                if device_dicts[device]['ctx_ver'] != None:
                    if device_dicts[device]['ctx_ver'] not in version_tracker[device_dicts[device]['dept']]['citrix']:
                        dict_series[device_dicts[device]['dept']]['ctx_ver_count'] += 1
                        version_tracker[device_dicts[device]['dept']]['citrix'].append(device_dicts[device]['ctx_ver'])
                if device_dicts[device]['zm_ver'] != None:
                    if device_dicts[device]['zm_ver'] not in version_tracker[device_dicts[device]['dept']]['zoom']:
                        dict_series[device_dicts[device]['dept']]['zm_ver_count'] += 1
                        version_tracker[device_dicts[device]['dept']]['zoom'].append(device_dicts[device]['zm_ver']) 
                if device_dicts[device]['wpl_ver'] != None:
                    if device_dicts[device]['wpl_ver'] not in version_tracker[device_dicts[device]['dept']]['build']:
                        dict_series[device_dicts[device]['dept']]['wpl_ver_count'] += 1
                        version_tracker[device_dicts[device]['dept']]['build'].append(device_dicts[device]['wpl_ver'])    
        return dict_series
    
    def dept_group_tagger(dept):
        dept_tags = {'Admin': ['AD_Viz_Data', 'AD_LP_Viz_Data'],
                     'Allergy': ['AI_Viz_Data', 'AI_LP_Viz_Data'],
                     'Conference': ['CONF2_Viz_Data', 'CONF3_Viz_Data', 'CONF4_Viz_Data', 'CONF_BK_Viz_Data'],
                     'Counseling': ['CS3_Viz_Data', 'CS4_Viz_Data', 'CS_BK_Viz_Data', 'CS_LP_Viz_Data'], 
                     'Facilities': ['FAC_Viz_Data', 'FAC_LP_Viz_Data'],
                     'Finance': ['FI_Viz_Data', 'FI_LP_Viz_Data'], 
                     'Global': ['GLOBAL_Viz_Data'],
                     'HPO':['HPO_Viz_Data', 'HPO_LP_Viz_Data'],
                     'Informatics': ['IF_Viz_Data', 'IF_LP_Viz_Data'], 
                     'IT': ['IT_Viz_Data', 'IT_LP_Viz_Data'], 
                     'Kitchen': ['KIT_Viz_Data'], 
                     'LiveWell': ['LW_Viz_Data', 'LW_LP_Viz_Data'], 
                     'Medical Records': ['MR_Viz_Data', 'MR_LP_Viz_Data'], 
                     'Moses': ['MC2_Viz_Data', 'MC3_Viz_Data', 'MC_BK_Viz_Data', 'MC_LP_Viz_Data'], 
                     'Nursing Hub': ['NH_Viz_Data', 'NH_LP_Viz_Data'], 
                     'OffSite': ['OFF_Viz_Data'], 
                     'Optometry': ['OPTO_Viz_Data', 'OPTO_LP_Viz_Data'], 
                     'Patient Accounts': ['PA_Viz_Data', 'PA_LP_Viz_Data'], 
                     'Pharmacy': ['PHA_Viz_Data', 'PHA_LP_Viz_Data'], 
                     'Popup Clinic': ['POPUP_Viz_Data'], 
                     'Primary Care': ['PC3_Viz_Data', 'PC4_Viz_Data', 'PC_BK_Viz_Data', 'PC_LP_Viz_Data'], 
                     'PSS': ['PSS_LP_Viz_Data'], 
                     'PT': ['PT_Viz_Data', 'PT_LP_Viz_Data'], 
                     'Specialty': ['SP_Viz_Data', 'SP_LP_Viz_Data'], 
                     'Wellness': ['WL_Viz_Data', 'WL_LP_Viz_Data'], 
                     'Womens Health': ['WH_Viz_Data', 'WH_LP_Viz_Data']}
        
        for tag in dept_tags:
            if dept in dept_tags[tag]:
                return tag
                
    def filter_laptops_tagger(dept):
        laptop_depts = ['AD_LP_Viz_Data', 'AI_LP_Viz_Data', 'CS_LP_Viz_Data', 'FAC_LP_Viz_Data',
                        'FI_LP_Viz_Data', 'HPO_LP_Viz_Data', 'IF_LP_Viz_Data', 'IT_LP_Viz_Data',
                        'LW_LP_Viz_Data', 'MR_LP_Viz_Data', 'MC_LP_Viz_Data', 'NH_LP_Viz_Data',
                        'OPTO_LP_Viz_Data', 'PA_LP_Viz_Data', 'PHA_LP_Viz_Data', 'PC_LP_Viz_Data',
                        'PT_LP_Viz_Data', 'SP_LP_Viz_Data', 'WL_LP_Viz_Data', 'WH_LP_Viz_Data']
        
        if dept in laptop_depts:
            return 'yes'
        else:
            return 'no'
    
    def filter_brooklyn_tagger(dept):
        brooklyn_depts = ['CONF_BK_Viz_Data', 'CS_BK_Viz_Data', 'MC_BK_Viz_Data', 'PC_BK_Viz_Data']
        
        if dept in brooklyn_depts:
            return 'yes'
        else:
            return 'no'

    def filter_726_tagger(dept):
        all_726_depts = ["AD_Viz_Data", "AI_Viz_Data", "CONF2_Viz_Data", "CONF3_Viz_Data", 
                         "CONF4_Viz_Data", "CS3_Viz_Data", "CS4_Viz_Data", "FAC_Viz_Data", 
                         "FI_Viz_Data", "HPO_Viz_Data", "IF_Viz_Data", "IT_Viz_Data", 
                         "KIT_Viz_Data", "LW_Viz_Data", "MC2_Viz_Data", "MC3_Viz_Data", 
                         "MR_Viz_Data", "NH_Viz_Data", "OPTO_Viz_Data", "PA_Viz_Data", 
                         "PC3_Viz_Data", "PC4_Viz_Data", "PHA_Viz_Data", "PT_Viz_Data", 
                         "SP_Viz_Data", "WH_Viz_Data", "WL_Viz_Data"]
        
        if dept in all_726_depts:
            return 'yes'
        else:
            return 'no'
    
    def filter_2_floor_tagger(dept):
        second_floor_depts = ["CONF2_Viz_Data", "MC2_Viz_Data"]
        
        if dept in second_floor_depts:
            return 'yes'
        else:
            return 'no'

    def filter_3_floor_tagger(dept):
        third_floor_depts = ["AI_Viz_Data", "CONF3_Viz_Data", "CS3_Viz_Data", "FAC_Viz_Data", 
                             "IF_Viz_Data", "IT_Viz_Data", "KIT_Viz_Data", "MC3_Viz_Data", 
                             "MR_Viz_Data", "NH_Viz_Data", "PA_Viz_Data", "PC3_Viz_Data", 
                             "SP_Viz_Data", "WL_Viz_Data"]
        
        if dept in third_floor_depts:
            return 'yes'
        else:
            return 'no'

    def filter_4_floor_tagger(dept):
        fourth_floor_depts = ["AD_Viz_Data", "CONF4_Viz_Data", "CS4_Viz_Data", "FI_Viz_Data", 
                              "HPO_Viz_Data", "LW_Viz_Data", "OPTO_Viz_Data", "PC4_Viz_Data", 
                              "PHA_Viz_Data", "PT_Viz_Data", "WH_Viz_Data"]
        
        if dept in fourth_floor_depts:
            return 'yes'
        else:
            return 'no'
    