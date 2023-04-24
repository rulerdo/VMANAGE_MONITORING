from modules.parser import load_yaml_config
from modules.vmanage import sdwan_manager
import json
from datetime import datetime
from pytz import timezone
import csv

def convert_epoc_to_pst(epoctime):
    date = datetime.fromtimestamp(epoctime, timezone('US/Central'))
    parsed_date = f'{str(date)[:-6]} CST'
    return parsed_date

if __name__ == '__main__':

    var = load_yaml_config('config/config.yaml')

    session = sdwan_manager(
        var['VMANAGE'],
        str(var['PORT']),
        var['USERNAME'],
        var['PASSWORD'])

    rules_set = [
        #{"value":["sla-change"], "field":"eventname", "type":"string", "operator": "in"},
        {"value":["168"], "field":"entry_time", "type":"string", "operator":"last_n_hours"}
        ]
    
    payload = json.dumps({"query": {"condition": "AND","rules": rules_set},"size": 10000})

    response = session.send_request(action='POST',resource=f'/event',body=payload)

    data = response.json()["data"]

    with open ('testfile.csv','w') as f:

        csv_writer = csv.writer(f)
        csv_writer.writerow(['Event Time', 'Hostname', 'System IP', 'Name', 'Severity', 'Component', 'Details'])
        all_events = []
        for event in data:
            startTime = str(event['entry_time'])[:-3]
            event["entry_time"] = convert_epoc_to_pst(int(startTime))
            new_row = [
                event["entry_time"],
                event["host_name"],
                event["system_ip"],
                event["eventname"],
                event["severity_level"],
                event["component"],
                event["details"],
            ]

            csv_writer.writerow(new_row)
            all_events.append(new_row)


names = ["bgp-peer-state-change",
"dhcp-address-renewed",
"sla-change",
"control-connection-tloc-ip-change",
"system-logout-change",
"system-login-change",
"interface-state-change",
"fib-updates",
"sla-violation",
"fib-update",
"system-aaa-login-fail",
"bfd-state-change"
]

for name in names:
    x = 0
    for event in all_events:
        if name in event:
            x += 1
        
    print(name, ':',x)