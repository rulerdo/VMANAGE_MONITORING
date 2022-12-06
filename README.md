# VMANAGE ALERTS

## Description

Set of scripts to assist with advanced monitoring for Cisco SDWAN

## Installation

Clone repository and use pip to install requirements

    pip install -r requirements.txt

## Configuration

There is a configuration files under config folder

    .
    ├─ config/
        └─ config.yaml

Edit File to provide the connection details to your environment

## Scripts

1. Report Example

This script will send a set of API calls to vmanage to collect information and create a report txt file with the general health of the network

    usage: report_example.py [-h] [--devices DEVICES] [--action {health_check,alarms,reachable,all}] [--hours HOURS] [--severity {Critical,Major,Medium,Minor}] [--verbose]

    Arguments for custom requests

    optional arguments:
    -h, --help            show this help message and exit
    --devices DEVICES     DeviceID for health check, if multiple separate with commas
    --action {health_check,alarms,reachable,all}
                            Select from the available actions to perform
    --hours HOURS         Filter the alarms based on the last N hours
    --severity {Critical,Major,Medium,Minor}
                            Filter the alarms based on the severity [Critical, Major, Minor], if multiple separate with commas
    --verbose             Print Results on Terminal

2. Webhook Example

This script is to enable a server to receive webhook notifications from vManage, it will receive the messages and send them back to the user via a Webex Message

    uvicorn webhook_example:app --host 0.0.0.0

3. Alarms per Device

This script will collect all the alarms for the device provided, if multiple separate with commas

    python alarms_per_device.py --device 1.1.1.1
    python alarms_per_device.py --device "1.1.1.1,2.2.2.2"

## References

    https://developer.cisco.com/docs/sdwan/


## Author

Raul Gomez

    rgomezbe@cisco.com
