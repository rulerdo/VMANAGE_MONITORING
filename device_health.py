from modules.parser import add_output, load_yaml_config, get_arguments, table_format, get_timestamp
from modules.vmanage import sdwan_manager


if __name__ == '__main__':

    var = load_yaml_config('config/config.yaml')
    args = get_arguments()
    timestamp = get_timestamp()
    filename = f'outputs/sdwan_device_health_report_{timestamp}.txt'
    report = open(filename,'w')

    session = sdwan_manager(
        var['VMANAGE'],
        str(var['PORT']),
        var['USERNAME'],
        var['PASSWORD'])

    # REACHABLE DEVICES
    print('Getting all reachable devices')
    headers = ['deviceId','host-name','reachability','device-type','device-model']
    all_devices = session.get_all_reachable_devices(headers)
    devices_table = table_format(all_devices,headers)

    # DEVICES STATUS
    print('Getting per device health status')
    devices = args.devices
    devices_status = session.get_devices_status(all_devices)
    status_table = table_format(devices_status,'firstrow')
    print('Complete!')

    # SAVE TO FILE AND / OR PRINT ON TERMINAL
    add_output(report,status_table,'DEVICES STATUS')
    print(status_table,'\n') if args.verbose else ''

    report.close()
    session.logout()