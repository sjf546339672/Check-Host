# coding: utf-8
from urllib import urlencode
import requests
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()


def check_result(result_ping, result_ssh, result_impi, vm_phy_result):
    """检查结果"""
    result_ping = json.loads(result_ping).values()[0]
    if result_ping == "true":
        result_ssh = json.loads(result_ssh).values()[0]
        if result_ssh == "true":
            return "采控代理异常"
        else:
            return "主机HANG住"
    else:
        if vm_phy_result != "物理机":
            print(111111111111)
            return vm_phy_result
        else:
            print(222222222222)
            print(result_impi)
            return result_impi

result_ping = json.dumps({"10.1.40.13":"true"})
result_ssh = json.dumps({"10.1.40.13": "false"})
result_impi = ""
vm_phy_result = ""

print check_result(result_ping, result_ssh, result_impi, vm_phy_result)
