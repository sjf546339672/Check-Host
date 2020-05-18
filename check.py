# coding: utf-8
import json
import platform
import socket
import os
import re
from urllib import urlencode
from urlparse import urljoin
import requests
from subprocess import Popen, PIPE, STDOUT, PIPE


class UyunCheck(object):

    def __init__(self, alert_id, res_id):
        self.id = alert_id
        self.res_id = res_id
        self.base_url = "http://10.1.240.109/"

    def create_alert(self):
        """创建告警"""
        apikey = "9cc4871e46094635a19d26557f9bb7f4"
        data = {
            "apikey": apikey,
            "app_key": "a8g645w6wdb99ovziohny5kf7ocekhbn"
        }
        body = {
                "severity": 3,
                "name": "testalert9",
                "description": "TestAlert",
                "entity_name": "10.1.1.1",
                "entity_addr": "10.1.62.172",
                "merge_key": "description",
                "identify_key": "ccid",
                "properties": [
                    {
                        "val": "5ea97cac33f3916b64834105",
                        "code": "ccid",
                        "name": "CCID"
                    }
                ]
            }
        request_data = urlencode(data)
        get_url = 'alert/openapi/v2/create?'
        url = self.base_url + get_url + request_data
        try:
            requests.post(url, data=json.dumps(body))
        except Exception as e:
            return

    def get_alert_number(self, alert_id):
        """获取计算告警的数量"""
        apikey = "e10adc3949ba59abbe56e057f2gg88dd"
        request_data = {
            "apikey": apikey,
            "pageSize": "10",
            "id": alert_id
        }
        data = urlencode(request_data)
        url = self.base_url + "alert/openapi/v2/incident/query?" + data
        try:
            response = requests.get(url)
            data = response.json()
            get_number = data["records"][0]["count"]
            return get_number
        except Exception as e:
            return

    def get_reource_type(self, res_id):
        data = {
            "apikey": "e10adc3949ba59abbe56e057f2gg88dd",
            "id": res_id,
        }
        request_data = urlencode(data)
        url = self.base_url + "store/openapi/v2/resources/get?" + request_data
        try:
            response = requests.get(url)
            json_response = response.json()
            resource_class_code = json_response["classCode"]
            print(resource_class_code)
            # if resource_class_code.lower() == "aix" or resource_class_code.lower() == "hpunix":
            #     print("带外 ip")
            #     ip = "10.1.100.14"
            # else:
            #     print("带内 ip")
            #     ip = "10.1.100.213"
            # return ip
        except Exception as e:
            return

    def run_cmd(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE, )
        stdout, _ = p.communicate()
        return p.returncode, stdout.strip()

    def ping_ip(self, ip_addr, echo_opened=True, echo_closed=False, num=1):
        """ping 测试"""
        is_open = False
        cmd = 'ping -{} {} {}'.format(
            'c' if platform.system() in ['Windows', 'Darwin'] else 'n', num,
            ip_addr)
        code, out = self.run_cmd(cmd)
        if re.search('ttl', out, re.I):
            is_open = True

        if is_open:
            if echo_opened:
                print '{:<15} opened'.format(ip_addr)
            return ip_addr
        else:
            if echo_closed:
                print '{:<15} closed'.format(ip_addr)

    def check_port(self, ip_addr, port):
        """检查端口"""
        try:
            s = socket.socket()
            s.connect((ip_addr, int(port)))
            s.close()
            print port, 'opened'
            return port
        except socket.error as e:
            return

    def check_ipmi(self, res_id):
        data = {
            # "classcode": "VM",
            "classcode": "PCServer",
        }
        request_data = urlencode(data)
        url = self.base_url + "/store/api/v1/metrics/detail/get?" + request_data
        headers = {
            "Cookie": "token=d4672fd690bafe70fe54d7bc0614c7059790a64067fe4556fce69f78195e8702;"
        }
        response = requests.get(url, headers=headers)
        print(response.status_code, response.content)

    def get_result_alert(self, result_ping, result_ssh, result_impi):
        apikey = "9cc4871e46094635a19d26557f9bb7f4"
        data = {
            "apikey": apikey,
            "app_key": "a8g645w6wdb99ovziohny5kf7ocekhbn"
        }
        body = {
            "severity": 3,
            "name": "testalert9",
            "description": "TestAlert",
            "entity_name": "10.1.1.1",
            "entity_addr": "10.1.62.172",
            "merge_key": "description",
            "identify_key": "ccid",
            "properties": [
                {
                    "val": "5ea97cac33f3916b64834105",
                    "code": "ccid",
                    "name": "CCID"
                }
            ]
        }
        request_data = urlencode(data)
        get_url = 'alert/openapi/v2/create?'
        url = self.base_url + get_url + request_data
        try:
            requests.post(url, data=json.dumps(body))
        except Exception as e:
            return


if __name__ == '__main__':
    alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
    res_id = "5ebf917c2350a90cacbbcc9d"
    uyun = UyunCheck(alert_id, res_id)
    # uyun.create_alert()  # 创建告警
    # uyun.get_alert_number(alert_id)  # 获取告警数量
    # uyun.get_reource_type(res_id)  # 获取资源类型
    # uyun.ping_ip("10.1.100.213")  # ping测试
    # uyun.check_port("10.1.100.213", 22)  # 检查端口
    # uyun.check_ipmi(res_id)
    # get_result_alert(111, 111, 111)



