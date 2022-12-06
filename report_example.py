from modules.parse_manager import add_output, load_yaml_config, get_arguments, get_all_reachable_devices, get_devices_status, get_alarms, get_table, get_timestamp
from modules.sdwan_manager import sdwan_manager


if __name__ == '__main__':

    var = load_yaml_config('config/config.yaml')
    args = get_arguments()
    timestamp = get_timestamp()
    filename = f'outputs/monitor_report_{timestamp}.txt'
    report = open(filename,'w')

    session = sdwan_manager(
        var['VMANAGE'],
        str(var['PORT']),
        var['USERNAME'],
        var['PASSWORD'])

    # REACHABLE DEVICES
    print('Getting all reachable devices')
    headers = ['deviceId','host-name','reachability','device-type','device-model']
    all_devices = get_all_reachable_devices(session,headers)
    devices_table = get_table(all_devices,headers)

    add_output(report,devices_table,'REACHABLE DEVICES')

    if args.verbose:
        print(devices_table,'\n')

    print('Complete')
    

    # DEVICES STATUS
    print('Getting devices status')
    if args.action in ['health_check','all']:
        devices = args.devices
        devices_status = get_devices_status(session,devices,all_devices)
        status_table = get_table(devices_status,'firstrow')
        
        add_output(report,status_table,'DEVICES STATUS')

        if args.verbose:
            print(status_table,'\n')

    print('Complete')

    # ALARMS
    print('Getting alarms')
    if args.action in ['alarms','all']:
        severity = args.severity.split(',')
        hours = str(args.hours)
        alarms_table,summary_table = get_alarms(session, severity, hours, all_devices)

        add_output(report,alarms_table,'ALARMS')
        add_output(report,summary_table,'ALARMS SUMMARY')

        if args.verbose:
            print(alarms_table,'\n')
            print(summary_table,'\n')

    print('Complete')

    # SAVE REPORT FILE
    report.close()
    print(f'File saved as {filename}!')

    session.logout()