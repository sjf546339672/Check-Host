# coding: utf-8
import json
import platform
import socket
import re
from urllib import urlencode
import requests
from subprocess import Popen, PIPE, STDOUT, PIPE


class UyunCheck(object):

    def __init__(self, alert_id, res_id):
        self.id = alert_id
        self.res_id = res_id
        self.base_url = "http://10.1.240.109/"
        self.apikey = "e10adc3949ba59abbe56e057f2gg88dd"
        self.app_key = "a8g645w6wdb99ovziohny5kf7ocekhbn"
        self.alert_apikey = "9cc4871e46094635a19d26557f9bb7f4"

    def create_alert(self):
        """创建告警"""
        data = {
            "apikey": self.alert_apikey,
            "app_key": self.app_key
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
            requests.post(url, json=body)
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

    def run_cmd(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE, )
        stdout, _ = p.communicate()
        return p.returncode, stdout.strip()

    def ping_ip(self, ip_addr, echo_opened=True, echo_closed=False, num=1):
        """ping 测试"""
        is_open = False
        cmd = 'ping -{} {} {}'.format('n' if platform.system() in ['Windows', 'Darwin'] else 'c', num,
            ip_addr)
        code, out = self.run_cmd(cmd)
        if re.search('ttl', out, re.I):
            is_open = True

        if is_open:
            if echo_opened:
                print '{:<15} opened'.format(ip_addr)
            return "true"
        else:
            if echo_closed:
                print '{:<15} closed'.format(ip_addr)
            return "false"

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

    def get_reource_type(self, res_id, apikey, vm_exector_ip, pc_exector_ip):
        """获取资源参数"""
        global os_ip
        global ping_ip
        global phy_res_id
        os_data = {"apikey": apikey, "id": res_id}
        os_request_data = urlencode(os_data)
        os_url = self.base_url + "store/openapi/v2/resources/get?" + os_request_data
        os_response = requests.get(os_url)
        os_content = os_response.json()
        if os_content["classCode"] not in ["VM", "PCServer"]:
            phy_url = "store/openapi/v2/resources/query_related?"
            phy_data = {"apikey": apikey}
            phy_request_data = urlencode(phy_data)
            phy_whole_url = self.base_url + phy_url + phy_request_data

            phy_headers = {'resource_id': res_id,
                           'Content-Type': 'application/json'}
            phy_condition = [{"field": "classCode", "operator": "IN",
                              "value": ['VM', 'PCServer', 'MiniServer']}]
            phy_body = {"conditions": phy_condition}
            try:
                phy_response = requests.post(url=phy_whole_url,
                                             headers=phy_headers, json=phy_body)
                phy_content = phy_response.json()
                phy_class_code_result = phy_content["dataList"][0]["classCode"]
                phy_res_id = phy_content["dataList"][0]["id"]
                os_ip = os_content["ip"]
                if phy_class_code_result == "VM":
                    print("带内")
                    ping_ip = vm_exector_ip
                else:
                    print("带外")
                    ping_ip = pc_exector_ip
                return os_ip, phy_res_id
            except Exception as e:
                return
        elif os_content["classCode"] in ["VM", "PCServer"]:
            os_class_code = os_content["classCode"]
            os_res_id = os_content["id"]
            phy_res_id = os_res_id
            if os_class_code == "VM":
                print("带内")
                ping_ip = vm_exector_ip
            else:
                print("带外")
                ping_ip = pc_exector_ip
            return os_ip, phy_res_id
        else:
            print("意外的参数值")

    def check_ipmi(self, res_id):
        """检查主机是否上电"""
        url = "store/openapi/v2/datapoints/query_last?"
        m = "ipmi.chassis.power.status"
        data = {
            'apikey': 'e10adc3949ba59abbe56e057f2gg88dd',
            'tag': 'object: {}'.format(res_id)
        }
        request_data = urlencode(data)
        whole_url = self.base_url + url + request_data
        headers = {'apikey': 'e10adc3949ba59abbe56e057f2gg88dd',
                   'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache'}

        response = requests.get(url=whole_url, headers=headers)
        for d in response.json():
            if d['metric'] == m:
                if str(d['value']) == "1.0":
                    return "true"
                elif str(d['value']) == "0.0":
                    return "false"

    def check_result(self, result_ping, result_ssh, result_impi):
        """检查结果"""
        if result_ping == "true":
            if result_ssh == "true":
                return "采控代理异常"
            else:
                return "HANG住了"
        else:
            if result_impi == "true":
                return "网络不可达"
            else:
                return "主机宕机"

    def alert_relate(self, parentId, childId):
        """创建父子告警关联"""
        data = {"apikey": self.apikey}

        body = {
            "parentId": parentId,
            "childs": [childId]
        }
        request_data = urlencode(data)
        url = "http://10.1.240.109/" + "alert/openapi/v2/incident/merge?" + request_data
        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }
        try:
            response = requests.post(url=url, json=body, headers=headers)
            print(response.status_code, response.content)
        except Exception as e:
            return

    def get_result_alert(self, result_ping, result_ssh, result_impi, ip):
        """创建一个新的告警"""
        data = {"apikey": self.apikey, "id": alert_id}
        request_data = urlencode(data)
        url = self.base_url + "alert/openapi/v2/incident/query?" + request_data
        response = requests.get(url)
        app_key = response.json()["records"][0]["appKey"]
        childid = response.json()["records"][0]["id"]

        result = self.check_result(result_ping, result_ssh, result_impi)

        create_data = {"apikey": self.alert_apikey, "app_key": app_key}
        create_body = {
            "severity": 3,
            "name": result,
            "description": result,
            "entity_name": "10.1.1.1",
            "entity_addr": ip,
        }
        create_request_data = urlencode(create_data)
        create_url = self.base_url + "alert/openapi/v2/create?" + create_request_data
        headers = {"Content-Type": "application/json;charset=utf-8"}
        try:
            requests.post(create_url, data=json.dumps(create_body),
                          headers=headers)
        except Exception as e:
            print(e)
            # alert_relate(parentid, childid)  # 创建的新告警id作为父 传进来的告警id子


if __name__ == '__main__':
    alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
    res_id = "5ebf917c2350a90cacbbcc9d"
    uyun = UyunCheck(alert_id, res_id)
    # uyun.create_alert()  # 创建告警
    # print uyun.get_alert_number(alert_id)  # 获取告警数量
    # uyun.get_reource_type(res_id)  # 获取资源类型
    # uyun.ping_ip("10.1.100.213")  # ping测试
    # uyun.check_port("10.1.100.213", 22)  # 检查端口
    # uyun.check_ipmi(res_id)  # 检查是否上电
    # uyun.get_result_alert(False, False, False)  # 创建新的告警创建
    # uyun.alert_relate()  # 建立父子关系