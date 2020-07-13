# coding: utf-8
import json
import platform
import socket
from urllib import urlencode
import requests
from subprocess import Popen, PIPE, STDOUT, PIPE


class UyunCheck(object):

    def __init__(self, alert_id, res_id):
        self.id = alert_id
        self.res_id = res_id
        # self.base_url = "http://10.1.240.109/"
        self.base_url = "https://10.1.40.111:7508/"
        self.apikey = "e10adc3949ba59abbe56e057f2gg88dd"
        self.app_key = "a8g645w6wdb99ovziohny5kf7ocekhbn"
        self.alert_apikey = "9cc4871e46094635a19d26557f9bb7f4"
        self.alert_id = alert_id

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

    def get_alert_number(self):
        """获取计算告警的数量"""
        request_data = {"apikey": self.apikey, "pageSize": "10", "id": self.alert_id}
        data = urlencode(request_data)
        url = self.base_url + "alert/openapi/v2/incident/query?" + data
        try:
            response = requests.get(url)
            data = response.json()
            get_number = data["records"][0]["count"]
            return get_number
        except Exception as e:
            return  #

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

    def get_reource_type(self, vm_exector_ip, pc_exector_ip):
        """获取资源参数"""
        global os_ip
        global ping_ip
        global phy_res_id
        os_data = {"apikey": self.apikey, "id": self.res_id}
        os_request_data = urlencode(os_data)
        os_url = self.base_url + "store/openapi/v2/resources/get?" + os_request_data
        os_response = requests.get(os_url)
        os_content = os_response.json()
        os_ip = os_content["ip"]
        if os_content["classCode"] not in ["VM", "PCServer"]:
            phy_url = "store/openapi/v2/resources/query_related?"
            phy_data = {"apikey": self.apikey}
            phy_request_data = urlencode(phy_data)
            phy_whole_url = self.base_url + phy_url + phy_request_data

            phy_headers = {'resource_id': self.res_id,
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

    def check_ipmi(self):
        """检查主机是否上电"""
        global get_ipmi_result
        url = "store/openapi/v2/datapoints/query_last?"
        m = "ipmi.chassis.power.status"
        data = {
            'apikey': self.apikey,
            'tag': 'object: {}'.format(self.res_id)
        }
        request_data = urlencode(data)
        whole_url = self.base_url + url + request_data
        headers = {'apikey': self.apikey, 'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache'}
        try:
            response = requests.get(url=whole_url, headers=headers)
            for d in response.json():
                if d['metric'] == m:
                    if str(d['value']) == "1.0":
                        get_ipmi_result = "true"
                    elif str(d['value']) == "0.0":
                        get_ipmi_result = "false"
            return get_ipmi_result
        except Exception as e:
            print("Check the failure")

    def check_result(self, result_ping, result_ssh, result_impi):
        """检查结果"""
        result_ping = json.loads(result_ping).values()[0]
        if result_ping == "true":
            result_ssh = json.loads(result_ssh).values()[0]
            if result_ssh == "true":
                return "采控代理异常"
            else:
                return "主机HANG住"
        else:
            if result_impi == "true":
                return "网络不可达"
            else:
                return "主机宕机"

    def alert_relate(self, parentId, childId):
        """创建父子告警关联"""
        data = {"apikey": self.apikey}
        body = {"parentId": parentId, "childs": [childId]}
        request_data = urlencode(data)
        url = "alert/openapi/v2/incident/merge?"
        whole_url = self.base_url + url + request_data
        try:
            requests.post(url=whole_url, json=body)
        except Exception as e:
            print(e)

    def get_result_alert(self, result_ping, result_ssh, result_impi, ip, ciid):
        """创建一个新的告警"""
        data = {"apikey": self.apikey, "id": self.alert_id}
        request_data = urlencode(data)
        url = self.base_url + "alert/openapi/v2/incident/query?" + request_data
        response = requests.get(url)
        app_key = response.json()["records"][0]["appKey"]
        childid = response.json()["records"][0]["id"]

        result = self.check_result(result_ping, result_ssh, result_impi)

        create_data = {
            "apikey": self.alert_apikey,
            "app_key": app_key,
            "properties": [
                {"val": ciid,
                 "code": "ciid",
                 "name": result
                 }]}

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
            response = requests.post(create_url, data=json.dumps(create_body), headers=headers)
            return response.status_code
        except Exception as e:
            print(e)
            # alert_relate(parentid, childid)  # 创建的新告警id作为父 传进来的告警id子


    def check_ipmi1(res_id):
        """检查主机是否上电"""
        global get_ipmi_result
        get_ipmi_result = ""
        url = "store/openapi/v2/datapoints/query_last?"
        m = "ipmi.chassis.power.status"
        data = {
            'apikey': apikey,
            'tag': 'object: {}'.format(res_id)
        }
        request_data = urlencode(data)
        whole_url = base_url + url + request_data
        headers = {'apikey': apikey, 'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache'}
        try:
            response = requests.get(url=whole_url, headers=headers,
                                    verify=False)
            print(response.status_code)
            print(response.json())
            for d in response.json():
                if d['metric'] == m:
                    if str(d['value']) == "1.0":
                        get_ipmi_result = "true"
                    elif str(d['value']) == "0.0":
                        get_ipmi_result = "false"
        except Exception as e:
            get_ipmi_result = "采控代理失联"
            print(e)
        return get_ipmi_result


def main():
    # alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
    alert_id = "5ef0209ad5de2de2e8a10d6e"
    # res_id = "5ecb29c82350a90cacbbcd71"
    res_id = "5ef01dc20381fd37821100bc"
    uyun = UyunCheck(alert_id, res_id)
    uyun.create_alert()  # 创建告警
    uyun.get_alert_number(alert_id)  # 获取告警数量
    uyun.get_reource_type(res_id)  # 获取资源类型
    uyun.ping_ip("10.1.100.213")  # ping测试
    uyun.check_port("10.1.100.213", 22)  # 检查端口
    uyun.check_ipmi(res_id)  # 检查是否上电
    uyun.get_result_alert(False, False, False)  # 创建新的告警创建
    uyun.alert_relate()  # 建立父子关系


if __name__ == '__main__':
    main()







