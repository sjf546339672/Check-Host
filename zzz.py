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

def check_ipmi(res_id):
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
        # print(response.json())
        list1 = response.json()
        list1 = [{'metric': "ipmi.chassis.power.status", 'value': 0.0}]
        print(list1)
        # for d in response.json():
        for d in list1:
            if d['metric'] == m:
                if str(d['value']) == "1.0":
                    print(111)
                    get_ipmi_result = "网络不可达"
                elif str(d['value']) == "0.0":
                    print(222)
                    get_ipmi_result = "主机宕机"
            else:
                print(333)
                get_ipmi_result = "采控代理失联"
        if list1 == []:
            print(444)
            get_ipmi_result = "采控代理失联"
    except Exception as e:
        print(555)
        get_ipmi_result = "采控代理失联"
        print(e)
    return get_ipmi_result

result_ping = json.dumps({"10.1.40.13":"true"})
result_ssh = json.dumps({"10.1.40.13": "false"})
result_impi = ""
vm_phy_result = ""

print check_result(result_ping, result_ssh, result_impi, vm_phy_result)
