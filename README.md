# VMANAGE ALERTS

## Description

Set of scripts to assist with advanced monitoring for Cisco SDWAN

## Installation

Clone repository and use pip to install requirements

    pip install -r requirements.txt

## Configuration

There is a configuration file under config folder

    .
    ├─ config/
        └─ config.yaml

Edit File to provide the connection details to your environment

## Scripts

### Device Health

Script to collect a general health status of all the devices on an SDWAN overlay

    usage: device_health.py [-h] [--devices DEVICES] [--hours HOURS] [--severity {Critical,Major,Medium,Minor}] [--verbose]

    Arguments for custom requests

    optional arguments:
    -h, --help            show this help message and exit
    --devices DEVICES     DeviceID for health check, if multiple separate with commas
    --hours HOURS         Filter the alarms based on the last N hours
    --severity {Critical,Major,Medium,Minor}
                            Filter the alarms based on the severity [Critical, Major, Medium, Minor], if multiple separate with commas
    --verbose             Print Results on Terminal

### Events Collector

This script will collect all the events from vManage

    usage: events_collector.py [-h] [--devices DEVICES] [--eventnames EVENTNAMES] [--components COMPONENTS] [--hours HOURS] [--severities SEVERITIES]
                            [--maxresults MAXRESULTS] [--showdevices] [--showevents] [--showcomponents]

    Arguments to filter collected events

    optional arguments:
    -h, --help            show this help message and exit
    --devices DEVICES     System IP to filter, if multiple separate with commas
    --eventnames EVENTNAMES
                            Event name to filter, if multiple separate with comma
    --components COMPONENTS
                            Components name to filter, if multiple separate with comma
    --hours HOURS         Filter the events based on the last N hours 1 day = 24 ; 1 week = 168
    --severities SEVERITIES
                            Severity to filter, if multiple separate with commas [Critical, Major, , Medium, Minor]
    --maxresults MAXRESULTS
                            Maximum number of results to collect
    --showdevices         Print available devices system IPs on terminal
    --showevents          Print available event names on terminal
    --showcomponents      Print available components system IPs on terminal

### Webhook Example

This script is to enable a server to receive webhook notifications from vManage, it will receive the messages and send them back to the user via a Webex Message

    uvicorn webhook_example:app --host 0.0.0.0

Expected endpoint: /webhook

## References

    https://developer.cisco.com/docs/sdwan/

## Author

Raul Gomez

    rgomezbe@cisco.com
