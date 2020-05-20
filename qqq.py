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


base_url = "http://10.1.240.109/"
alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
res_id = "5ebf917c2350a90cacbbcc9d"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"


def create_alert():
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
    url = base_url + get_url + request_data
    try:
        requests.post(url, data=json.dumps(body))
    except Exception as e:
        return


def get_alert_number(alert_id):
    """获取计算告警的数量"""
    apikey = "e10adc3949ba59abbe56e057f2gg88dd"
    request_data = {
        "apikey": apikey,
        "pageSize": "10",
        "id": alert_id
    }
    data = urlencode(request_data)
    url = base_url + "alert/openapi/v2/incident/query?" + data
    try:
        response = requests.get(url)
        data = response.json()
        get_number = data["records"][0]["count"]
        return get_number
    except Exception as e:
        return


# print(get_alert_number(alert_id))

def get_reource_type(res_id):
    """获取资源参数"""
    # 入参 res_id, apikey
    # 出参 os_ip phy_ip  phy_res_id
    os_data = {
        "apikey": apikey,
        "id": res_id
    }
    os_request_data = urlencode(os_data)
    os_url = base_url + "store/openapi/v2/resources/get?" + os_request_data
    os_response = requests.get(os_url)
    os_content = os_response.json()
    if os_content["classCode"] != "VM" or os_content["classCode"] != "PCServer":
        phy_url = "store/openapi/v2/resources/query_related?"
        phy_data = {"apikey": apikey}
        phy_request_data = urlencode(phy_data)
        phy_whole_url = base_url + phy_url + phy_request_data

        phy_headers = {'resource_id': res_id, 'Content-Type': 'application/json'}
        phy_condition = [{"field": "classCode", "operator": "IN", "value": ['VM', 'PCServer', 'MiniServer']}]
        phy_body = {"conditions": phy_condition}

        try:
            phy_response = requests.post(url=phy_whole_url, headers=phy_headers,
                                         json=phy_body)
            phy_content = phy_response.json()
            phy_class_code_result = phy_content["dataList"][0]["classCode"]
            phy_res_id = phy_content["dataList"][0]["id"]
            phy_ip = phy_content["dataList"][0]["OS_IP"]
            os_ip = os_content["ip"]
            if phy_class_code_result == "VM":
                print("带内")
            else:
                print("带外")
            return os_ip, phy_ip, phy_res_id
        except Exception as e:
            return

# print(get_reource_type(res_id))


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE, )
    stdout, _ = p.communicate()
    return p.returncode, stdout.strip()


def ping_ip(ip_addr, echo_opened=True, echo_closed=False, num=1):
    """ping 测试"""
    is_open = False
    cmd = 'ping -{} {} {}'.format(
        'c' if platform.system() in ['Windows', 'Darwin'] else 'n', num,
        ip_addr)
    code, out = run_cmd(cmd)
    if re.search('ttl', out, re.I):
        is_open = True

    if is_open:
        if echo_opened:
            print '{:<15} opened'.format(ip_addr)
        return ip_addr
    else:
        if echo_closed:
            print '{:<15} closed'.format(ip_addr)
# ping_ip("10.1.100.213")


def check_port(ip_addr, port):
    """检查端口"""
    try:
        s = socket.socket()
        s.connect((ip_addr, int(port)))
        s.close()
        print port, 'opened'
        return port
    except socket.error as e:
        return


def check_ipmi(res_id):
    """检查主机是否上电"""
    url = "store/openapi/v2/datapoints/query_last?"
    m = "ipmi.chassis.power.status"
    data = {
        'apikey': 'e10adc3949ba59abbe56e057f2gg88dd',
        'tag': 'object: {}'.format(res_id)
    }
    request_data = urlencode(data)
    whole_url = base_url + url + request_data
    headers = {'apikey': 'e10adc3949ba59abbe56e057f2gg88dd',
               'Content-Type': 'application/json',
               'Cache-Control': 'no-cache'}

    response = requests.get(url=whole_url, headers=headers)
    for d in response.json():
        if d['metric'] == m:
            if str(d['value']) == "1.0":
                return True
            elif str(d['value']) == "0.0":
                return False


def check_result(result_ping, result_ssh, result_impi):
    """检查结果"""
    if result_ping is True:
        if result_ssh is True:
            return "采控代理异常"
        else:
            return "HANG住了"
    else:
        if result_impi is True:
            return "网络不可达"
        else:
            return "主机宕机"


def get_result_alert(result_ping, result_ssh, result_impi):
    """创建一个新的告警"""
    result = check_result(result_ping, result_ssh, result_impi)
    print(result)
    apikey = "9cc4871e46094635a19d26557f9bb7f4"
    data = {
        "apikey": apikey,
        "app_key": "a8g645w6wdb99ovziohny5kf7ocekhbn"
    }
    body = {
        "severity": 3,
        "name": result,
        "description": "Alert",
        "entity_name": "10.1.1.1",
    }
    request_data = urlencode(data)
    get_url = 'alert/openapi/v2/create?'
    url = base_url + get_url + request_data
    try:
        response = requests.post(url, data=json.dumps(body))
        print(url)
        print(response.status_code)
        print(response.content)
    except Exception as e:
        return


def alert_relate():
    """创建父子告警关联"""
    # alert13 = "06b7742634d0eea11c3d614ccd676b80"
    # alert3 = "193fe81c529f4391c9610f548fe765bc"
    data = {
         "apikey": "e10adc3949ba59abbe56e057f2gg88dd"
    }

    body = {
        "parentId": "ad45bb4d9abe4dae8bf8022bef996c39",
        "childs": ["652748480d03482fb9048bdf7cfa4296"]
    }
    request_data = urlencode(data)
    url = "alert/openapi/v2/incident/merge?"
    url = "http://10.1.240.109/" + url + request_data
    print(url)
    response = requests.post(url=url, json=body)
    print(response.status_code, response.content)  #


# create_alert()  # 创建告警
# print get_alert_number(alert_id)  # 获取告警数量
# get_reource_type(res_id)  # 获取资源类型
# ping_ip("10.1.100.213")  # ping测试
# check_port("10.1.100.213", 22)  # 检查端口
# check_ipmi(res_id)  # 检查是否上电
# get_result_alert(False, False, False)  # 创建新的告警创建
# alert_relate()  # 建立父子关系











