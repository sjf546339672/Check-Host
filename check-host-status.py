# coding: utf-8
import json
import socket
import urllib

import os
from urllib.parse import urlencode
import requests


def start(id, res_id):
    request_data = {
        "apikey": "e10adc3949ba59abbe56e057f2gg88dd",
        "pageSize": "10",
        "id": id
    }
    data = urlencode(request_data)
    alert_url = "http://10.1.61.237/alert/openapi/v2/incident/query?"+data
    get_number = get_alert_number(alert_url)
    print(get_number)
    # if get_number <= 50:
    #     pass


def get_alert_number(url):
    """获取计算告警的数量"""
    response = requests.get(url)
    data = response.json()
    get_number = data["records"][0]["count"]
    return get_number


def get_excutor_machine():
    """查询资源类型"""
    base_url = "http://10.1.200.204/store/openapi/v2/resources/get?"
    data = {
        "apikey": "",
        "id": "",
    }
    request_data = urlencode(data)
    url = base_url+request_data  # 根据ID获取对应的资源对象详情(资源类型名称)
    response = requests.get(url)
    print(response.status_code, response.json())
    resource_name = response.json()["className"]  # 查询资源类型名称
    return resource_name


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


def check_impi(res_id):
    base_url = "http://10.1.240.109/store/api/v1/metrics/detail/get?"
    data = {
        "classcode": "PCServer",
        # "_": "1589287313068"
    }
    request_data = urlencode(data)
    url = base_url + request_data
    print(url)
    headers = {
        "Cookie": "token=71edb66f59d4e1e21e683e11542ac25816dd800152b0cd5cfa265efb97cadd26;"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.content)


check_impi("111")


def chack_host_status(ip_addr, port):
    get_ping_result = ping_ip(ip_addr)
    if get_ping_result is True:
        get_port_result = check_prot(ip_addr, port)
        if get_port_result is True:
            print("采控异常")
        else:
            print("HANG死")
    else:
        pass


def main():
    pass


if __name__ == '__main__':
    main()






