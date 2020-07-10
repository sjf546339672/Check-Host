# coding: utf-8
import json
import platform
import socket
from urllib import urlencode, unquote
import requests
from subprocess import Popen, PIPE, STDOUT, PIPE
import ssl


class UyunCheck(object):

    def __init__(self, res_id):
        self.res_id = res_id
        self.base_url = "https://10.1.40.111:7508/"
        self.apikey = "e10adc3949ba59abbe56e057f2gg88dd"
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_reource_type(self, vm_exector_ip):
        """获取资源参数"""
        os_data = {"apikey": self.apikey, "id": self.res_id}
        os_request_data = urlencode(os_data)
        os_url = self.base_url + "store/openapi/v2/resources/get?" + os_request_data
        os_response = requests.get(os_url, verify=False)
        os_content = os_response.json()
        os_ip = os_content["ip"]
        if os_content["classCode"] not in ["VM", "PCServer"]:
            phy_url = "store/openapi/v2/resources/query_related?"
            phy_data = {"apikey": self.apikey}
            phy_request_data = urlencode(phy_data)
            phy_whole_url = self.base_url + phy_url + phy_request_data

            phy_headers = {'resource_id': self.res_id, 'Content-Type': 'application/json'}
            phy_condition = [{"field": "classCode", "operator": "IN", "value": ['VM', 'PCServer', 'MiniServer']}]
            phy_body = {"conditions": phy_condition}
            try:
                phy_response = requests.post(url=phy_whole_url,  headers=phy_headers, json=phy_body, verify=False)
                phy_content = phy_response.json()
                phy_class_code_result = phy_content["dataList"][0]["classCode"]
                phy_res_id = phy_content["dataList"][0]["id"]
                ping_ip = vm_exector_ip
                return os_ip, phy_res_id, phy_class_code_result
            except Exception as e:
                print(e)
                check_relation = 'false'
                return check_relation
        elif os_content["classCode"] in ["VM", "PCServer"]:
            os_class_code = os_content["classCode"]
            os_res_id = os_content["id"]
            phy_res_id = os_res_id
            ping_ip = vm_exector_ip
            return os_ip, phy_res_id, os_class_code

    def run_cmd(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE, )
        stdout, _ = p.communicate()
        return p.returncode, stdout.strip()

    def ping_ip(self, ip_addr, num=1, timeout=5):
        """ping 测试"""
        cmd = 'ping -{} {} {}'.format('n' if platform.system() in ['Windows', 'Darwin'] else 'c', num, ip_addr)
        code, out = self.run_cmd(cmd)
        if code == 0:
            get_ping_result = "true"
        else:
            get_ping_result = "false"
        return get_ping_result

    def check_port(self, ip_addr, port):
        """检查端口"""
        try:
            s = socket.socket()
            s.connect((ip_addr, int(port)))
            s.close()
            print port, 'opened'
            get_port_result = "true"
        except socket.error as e:
            get_port_result = "false"
        return get_port_result

    def check_ipmi(self):
        """检查主机是否上电"""
        global get_ipmi_result
        url = "store/openapi/v2/datapoints/query_last?"
        m = "ipmi.chassis.power.status"
        data = {'apikey': self.apikey, 'tag': 'object: {}'.format(self.res_id)}
        request_data = urlencode(data)
        whole_url = self.base_url + url + request_data
        headers = {'apikey': self.apikey, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
        try:
            response = requests.get(url=whole_url, headers=headers, verify=False)
            for d in response.json():
                if d['metric'] == m:
                    if str(d['value']) == "1.0":
                        get_ipmi_result = "true"
                    elif str(d['value']) == "0.0":
                        get_ipmi_result = "false"
            return get_ipmi_result
        except Exception as e:
            print("Check the failure", e)

    def check_vm_or_pm(self, host_type, check_relation):
        result = ''
        if check_relation == 'true':
            result = "代理失联"
        else:
            if host_type == 'VM':
                result = "主机宕机"
            elif host_type == 'PCServer':
                check_ipmi_result = self.check_ipmi()
                if check_ipmi_result == "true":
                    result = "主机宕机, 网络不可达"
                else:
                    result = "主机宕机, 代理失联"
        return result


def main():
    # alert_id = "632c28fdc12041fbb735d61522abb768"
    res_id = "5ef01dc20381fd37821100bc"
    uyun = UyunCheck(res_id)

    # 获取资源参数
    vm_exector_ip = '10.1.40.13'  # 带内ip
    # get_reource_result = uyun.get_reource_type(vm_exector_ip) # (u'10.1.100.213', u'5ef01dc30381fd37821100c0', u'VM')
    # get_ping_result = uyun.ping_ip(get_reource_result[0])  # true or false
    # get_port_result = uyun.check_port(get_reource_result[0], 22) # true or false
    # print uyun.get_reource_type('10.1.40.13')
    uyun.check_vm_or_pm('PCServer', 'true')


if __name__ == '__main__':
    main()





