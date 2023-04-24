from argparse import ArgumentParser
import yaml
import json
from tabulate import tabulate
from datetime import datetime
from ipaddress import ip_address
import sys


def confirm_is_IP(text):

    try:
        ip_address(text)
        return True

    except ValueError:
        return False


def get_title(action):
    size = 80
    title = '=' * size + "\n" + action.center(size) + "\n" + '=' * size + "\n" 
    return title


def add_output(report,table,title):

    message = get_title(title) + table + '\n'    
    report.write(message)


def get_arguments():

    parser = ArgumentParser(description='Arguments for custom requests')
    parser.add_argument('--devices', default='All_devices', help='DeviceID for health check, if multiple separate with commas')
    parser.add_argument('--hours', default=24, type=int, help='Filter the alarms based on the last N hours')
    parser.add_argument('--severity', default='Major', choices=["Critical", "Major", "Medium", "Minor"], help='Filter the alarms based on the severity [Critical, Major, Medium, Minor], if multiple separate with commas')
    parser.add_argument('--verbose', action="store_true", help="Print Results on Terminal")
    arguments = parser.parse_args()

    return arguments


def load_yaml_config(config_file):

    with open(config_file, 'r') as f:
        variables = yaml.safe_load(f)

    for key in variables.keys():
        if not variables[key]:
            variables[key] = input(f'{key}: ')

    return variables


def get_all_cloud_edges(all_reachable_devices):

    all_cloud_edges = list()
    for line in all_reachable_devices:
        if 'vedge' in line and 'vedge-ASR-1002-HX' not in line:
            all_cloud_edges.append(line)

    return all_cloud_edges


def get_hostnames_from_systemIPs(systemIPs,all_reachable_devices):

    devices_names = dict()
    for line in systemIPs:
        for row in all_reachable_devices:
            if line in row:
                devices_names[line] = row[1]

    return devices_names


def get_alarms_single_device(session, severity, hours, device):
    
    rules_set = [
        {"value":[device], "field":"system_ip", "type":"string", "operator": "in"},
        {"value":["CPU_Usage"], "field":"rule_name_display", "type":"string", "operator": "in"},
        {"value":severity, "field":"severity", "type":"string", "operator":"in"},
        {"value":[hours], "field":"entry_time", "type":"string", "operator":"last_n_hours"},
    ]

    query = json.dumps({"query": {"condition": "AND","rules": rules_set},"size": 10000})

    response = session.send_request('GET',f'/alarms?query={query}',body = {})
    data = response.json()['data']

    headers = ['SYSTEM IP','HOSTNAME','RULENAME','MESSAGE','EVENT TIME','SEVERITY']
    alarms_list = []
    
    for alarm in data:
        system_ip = alarm['values'][0]['system-ip']
        hostname = alarm['values'][0]['host-name']
        rulename = alarm['rulename']
        message = alarm['message']
        epoch_time = int(alarm['entry_time']/1000)
        eventtime = str(datetime.fromtimestamp(epoch_time))
        sev = alarm['severity']
        new_row = [system_ip,hostname,rulename,message,eventtime,sev]
        alarms_list.append(new_row)

    if alarms_list:
        return tabulate(alarms_list,headers,tablefmt='pretty')

    return None


def get_alarms(session, severity, hours, all_devices):
 
    rules_set = [
        {"value":["CPU_Usage"], "field":"rule_name_display", "type":"string", "operator": "in"},
        {"value":severity, "field":"severity", "type":"string", "operator":"in"},
        {"value":[hours], "field":"entry_time", "type":"string", "operator":"last_n_hours"},
    ]

    query = json.dumps({"query": {"condition": "AND","rules": rules_set},"size": 10000})

    response = session.send_request('GET',f'/alarms?query={query}',body = {})
    try:
        data = response.json()['data']
    except:
        print(response.text)
        print(response.status_code)
        sys.exit(1)
    headers = ['SYSTEM IP','HOSTNAME','RULENAME','MESSAGE','EVENT TIME','SEVERITY']
    alarms_list = []
    
    for alarm in data:
        system_ip = alarm['values'][0]['system-ip']
        hostname = alarm['values'][0]['host-name']
        rulename = alarm['rulename']
        message = alarm['message']
        epoch_time = int(alarm['entry_time']/1000)
        eventtime = str(datetime.fromtimestamp(epoch_time))
        sev = alarm['severity']
        new_row = [system_ip,hostname,rulename,message,eventtime,sev]
        alarms_list.append(new_row)

    devices = set([line[0] for line in alarms_list])
    devices_names = get_hostnames_from_systemIPs(devices,all_devices)

    alarms_table = tabulate(alarms_list,headers,tablefmt='pretty')
    
    counter = dict()
    for device in devices:
        counter[device] = 0
        for line in alarms_list:
            if device in line:
                counter[device] += 1

    sorted_summary = ({k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)})
    summary = [['SYSTEM-IP', 'HOSTNAME', '# ALARMS']]
    for key,value in sorted_summary.items() :
        new_row = (key,devices_names[key],value)
        summary.append(new_row)
    
    summary_table = tabulate(summary,headers='firstrow',tablefmt='pretty')

    return alarms_table, summary_table


def table_format(list,headers):
    return tabulate(list,headers=headers,tablefmt='pretty')


def get_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')