import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from time import time


class sdwan_manager():


    def __init__(self,server,port,username,password):

        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.host = server + ':' + port
        self.cookie = self.get_auth_cookie()
        self.token = self.get_auth_token()

    
    def get_auth_cookie(self):

        url = f"https://{self.host}/j_security_check"

        payload = f'j_username={self.username}&j_password={self.password}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        cookie = response.cookies.get_dict()['JSESSIONID']

        return cookie


    def get_auth_token(self):

        url = f"https://{self.server}/dataservice/client/token"

        payload={}
        headers = {
        'Cookie': f'JSESSIONID={self.cookie}'
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        token = response.text

        return token


    def send_request(self,action,resource,body):

        url = f'https://{self.host}/dataservice{resource}'

        headers = {
        'X-XSRF-TOKEN': self.token,
        'Cookie': f'JSESSIONID={self.cookie}',
        'Content-Type': 'application/json',
        }

        response = requests.request(action, url, headers=headers, data=body, verify=False)

        return response
                

    def logout(self):

        url = f"https://{self.host}/logout?nocache={str(int(time()))}"

        payload={}

        headers = {
        'Cookie': f'JSESSIONID={self.cookie}',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        message = 'vManage session closed!' if response.status_code == 200 else 'Problems closing session'
        print(message)


    def get_all_reachable_devices(self,headers):

        response = self.send_request('GET','/device',body = {})
        data = response.json()['data']

        all_reachable_devices = list()
        for element in data:
            new_row = list()
            for k,v in element.items():
                if k in headers:
                    new_row.append(v)

            if 'unreachable' not in new_row:
                all_reachable_devices.append(new_row)

        return all_reachable_devices


    def get_devices_status(self,all_reachable_devices):
        
        headers = ['SYSTEM IP', 'HOSTNAME', 'UP TIME', 'MEM USE', 'DISK USE','CPU USE']
        status_table = [headers]

        for line in all_reachable_devices:

            try:
                deviceID = line[0]
                response = self.send_request('GET',f'/device/system/status?deviceId={deviceID}',body = {})
                data = response.json()['data'][0]
                mem_use = str(round(int(data['mem_used']) * 100 / int(data['mem_total']),2)) + ' %'
                disk_use = data['disk_use'] + ' %'
                cpu_use = str(round(100 - float(data['cpu_idle']),2)) + ' %'
                new_row = [data['vdevice-name'], data['vdevice-host-name'], data['uptime'],mem_use, disk_use, cpu_use]

            except:
                deviceIDerror = deviceID[0] + '*'
                new_row = [deviceIDerror]
                for _ in range(len(headers)-1):
                    new_row.append(None)

            status_table.append(new_row)

        return status_table