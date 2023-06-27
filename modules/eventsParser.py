import yaml
import json
import csv
import sys
import os
from pytz import timezone
from datetime import datetime
from argparse import ArgumentParser
from tabulate import tabulate
from getpass import getpass


def parse_filter_rules(devices,eventnames,severity,hours,max_results,components):

    device_rule = {"value":devices, "field":"system_ip", "type":"string", "operator": "in"}
    event_rule = {"value":eventnames, "field":"eventname", "type":"string", "operator": "in"}
    component_rule = {"value":components, "field":"component", "type":"string", "operator": "in"}
    severity_rule = {"value":severity, "field":"severity", "type":"string", "operator":"in"}
    hours_rule = {"value":hours, "field":"entry_time", "type":"string", "operator":"last_n_hours"}

    rules_set = []

    if devices: rules_set.append(device_rule)
    if eventnames: rules_set.append(event_rule)
    if components: rules_set.append(component_rule)
    if severity: rules_set.append(severity_rule)
    if hours: rules_set.append(hours_rule)

    payload = json.dumps({"query": {"condition": "AND","rules": rules_set},"size": max_results})

    return payload


def save_csv(filename,data):

    if not data:
        print('No data found for given filters!')
        sys.exit(1)

    with open (filename,'w') as f:

        csv_writer = csv.writer(f)
        csv_writer.writerow(['Event Time', 'Hostname', 'System IP', 'Name', 'Severity', 'Component', 'Details'])
        all_events = []
        for event in data:
            startTime = str(event['entry_time'])[:-3]
            event["entry_time"] = convert_epoc_to_tz(int(startTime),'US/Central','CST')
            new_row = [
                event["entry_time"],
                event["host_name"],
                event["system_ip"],
                event["eventname"],
                #event["severity_level"],
                event["component"],
                event["details"],
            ]

            csv_writer.writerow(new_row)
            all_events.append(new_row)

    print('File saved as:',filename)


def convert_epoc_to_tz(epoctime,tz,acronym):
    date = datetime.fromtimestamp(epoctime, timezone(tz))
    parsed_date = f'{str(date)[:-6]} {acronym}'
    return parsed_date


def get_arguments():

    parser = ArgumentParser(description='Arguments to filter collected events')
    parser.add_argument('--devices', default=None, help='System IP to filter, if multiple separate with commas')
    parser.add_argument('--eventnames', default=None, type=str, help='Event name to filter, if multiple separate with comma')
    parser.add_argument('--components', default=None, type=str, help='Components name to filter, if multiple separate with comma')
    parser.add_argument('--hours', default="24", type=str, help='Filter the events based on the last N hours 1 day = 24 ; 1 week = 168')
    parser.add_argument('--severities', default=None, help='Severity to filter, if multiple separate with commas [Critical, Major, , Medium, Minor]')
    parser.add_argument('--maxresults', default=10000, type=int, help='Maximum number of results to collect')
    parser.add_argument('--showdevices', action="store_true", help="Print available devices system IPs on terminal")
    parser.add_argument('--showevents', action="store_true", help="Print available event names on terminal")
    parser.add_argument('--showcomponents', action="store_true", help="Print available components system IPs on terminal")
    arguments = parser.parse_args()

    return arguments


def load_yaml_config(config_file):

    with open(config_file, 'r') as f:
        variables = yaml.safe_load(f)

    for key in variables.keys():
        if not variables[key]:
            if key == 'PASSWORD':
                variables[key] = getpass(f'{key}: ')
            else:
                variables[key] = input(f'{key}: ')

    return variables


def create_filename():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    modules = os.path.dirname(__file__)
    outputs = os.path.join(os.path.dirname(modules), "outputs")
    filename = os.path.join(outputs, f'VMANAGE-EVENTS--{timestamp}.csv')
    return filename


def get_all_devices(response):

    all_devices = []
    for device in response.json()['data']:
        if device['personality'] not in ['vmanage','vsmart','vbond']:
            all_devices.append([device['system-ip'],device['host-name']])

    return all_devices


def get_all_components(response):

    all_components = [[line['value']] for line in response.json()['data']]

    return all_components


def get_all_event_names(response):

    all_events = [[line['value']] for line in response.json()['data']]

    return all_events


def get_table(list,headers,alignment='center'):
    return tabulate(list,headers=headers,tablefmt='pretty',colalign=({alignment},))
