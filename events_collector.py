from modules.vmanage import sdwan_manager
from modules.eventsParser import (
    load_yaml_config,
    get_arguments,
    save_csv,
    parse_filter_rules,
    create_filename,
    get_all_event_names,
    get_all_devices,
    get_all_components,
    get_table,
    )


if __name__ == '__main__':

    try:

        args = get_arguments()
        var = load_yaml_config('config/config.yaml')

        host = var['VMANAGE']
        port = str(var['PORT'])
        user = var['USERNAME']
        pwd = var['PASSWORD']
        session = sdwan_manager(host,port,user,pwd)

        if args.showdevices:

            response = session.send_request(action='GET',resource=f'/device',body={})
            all_devices = get_all_devices(response)
            print(get_table(all_devices,headers=['SYSTEM IP', 'HOSTNAME'],alignment='center'))
            session.logout()

        elif args.showevents:
            response = session.send_request(action='GET',resource=f'/event/types/keyvalue',body={})
            all_events = get_all_event_names(response)
            print(get_table(all_events,headers=['AVAILABLE EVENT NAMES'],alignment='left'))

        elif args.showcomponents:
            response = session.send_request(action='GET',resource=f'/event/component/keyvalue',body={})
            all_components = get_all_components(response)
            print(get_table(all_components,headers=['AVAILABLE COMPONENT NAMES'],alignment='left'))
        
        else:

            eventnames = args.eventnames.split(',') if args.eventnames else None
            devices = args.devices.split(',') if args.devices else None
            severities = args.severities.split(',') if args.severities else None
            components = args.components.split(',') if args.components else None

            hours = [args.hours]
            max_results = args.maxresults

            payload = parse_filter_rules(
                devices,
                eventnames,
                severities,
                hours,
                max_results,components)

            response = session.send_request(action='POST',resource=f'/event',body=payload)

            data = response.json()["data"]

            filename = create_filename()

            save_csv(filename,data)
    
            session.logout()

    except Exception as error:
        print('Execution Error')
        print(error)