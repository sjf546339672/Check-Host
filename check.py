# coding: utf-8
import json
import socket
from urllib.parse import urlencode
from urllib.request import urlopen

import os
import requests
from requests import Request


ip = "10.1.200.204"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"


def test_create_alert():
    """获取创建告警"""
    base_url = "http://{}/alert/openapi/v2/create?".format(ip)
    data = {
        "apikey": apikey,
        "app_key": "a40c2128nvln299f88sw162g3ms4uj53"
    }
    body = {
        "severity": 3,
        "name": "testalert3",
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
    url = base_url + request_data
    response = requests.post(url, data=json.dumps(body))
    print(response.status_code)
    print(response.content)


def get_alert_number(alert_id):
    """获取计算告警的数量"""
    request_data = {
        "apikey": apikey,
        "pageSize": "10",
        "id": alert_id
    }
    data = urlencode(request_data)
    alert_url = "http://{}/alert/openapi/v2/incident/query?".format(ip) + data
    response = requests.get(alert_url)
    try:
        data = response.json()
        get_number = data["records"][0]["count"]
        return get_number
    except Exception as e:
        print(e)


def get_reource_type(res_id):
    base_url = "http://devops.uyunsoft.cn/store/openapi/v2/resources/get?"
    data = {
        "apikey": "a6b367e9c5724b8c98a60ffa1572b563",
        "id":  res_id,
    }
    request_data = urlencode(data)
    url = base_url + request_data  # 根据ID获取对应的资源对象详情(资源类型名称)
    headers = {
        "Cookie": "token=82f9ffef6d67785846a6374b9b27af42406a6d1fbc51798227d42ba8c494d51a"
    }
    response = requests.get(url, headers=headers)
    try:
        resource_name = response.json()["className"]  # 查询资源类型名称
        resource_ip = response.json()["ip"]
        resource_class_code = response.json()["classCode"]
        return resource_name, resource_ip, resource_class_code
    except Exception as e:
        print(e)


def ping_ip(ip_addr):
    result = os.popen('ping -n 1 ' + ip_addr, 'r')
    shuchu = result.read()
    result.close()
    if not shuchu.count('请求超时'):
        return True
    else:
        return False


def check_prot(ip_addr, port):
    """检测远程端口是否正常"""
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip_addr, port))
        print('Server port {} OK!'.format(port))
        return True
    except Exception:
        print('Server port {} not connect!'.format(port))
        return False


def main(alert_id, res_id):
    get_number = get_alert_number(alert_id)
    if get_number <= 50:
        resource_name = get_reource_type(res_id)[0]
        resource_ip = get_reource_type(res_id)[1]
        resource_class_code = get_reource_type(res_id)[3]
        if resource_name == "虚拟机":
            print("带内", resource_name, resource_ip)
            ping_result = ping_ip(resource_ip)
            if ping_result is True:
                check_prot_result = check_prot(resource_ip, "8080")
                if check_prot_result is True:
                    print("采控异常")
                else:
                    print("HANG住了")
            else:
                pass
        else:
            print("带外", resource_name, resource_ip)


if __name__ == '__main__':
    alert_id = "5ebf971844d9e79b29ab4039"
    res_id = "5e5f4347438042e42641a5d1"
    main(alert_id, res_id)



