from modules.parser import add_output, load_yaml_config, get_arguments,get_alarms_single_device,get_timestamp,confirm_is_IP
from modules.vmanage import sdwan_manager

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

    # GET ALARMS
    print('Getting alarms')

    devices = args.devices.split(',')

    for ip in devices:
        if confirm_is_IP(ip):
            alarms_table = get_alarms_single_device(session,["Critical", "Major", "Medium" , "Minor"], "24", ip)
            if alarms_table:
                add_output(report,alarms_table,f'ALARMS FOR {ip}')
                if args.verbose:
                    print(alarms_table,'\n')
            else:
                print('No alarms found for', ip)
        else:
            print(ip, 'is not a valid IP!')

    print('Complete')
