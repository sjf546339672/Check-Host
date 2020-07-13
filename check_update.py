# coding: utf-8
base_url = "https://10.1.40.111:7508/"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"
vm_exector_ip = "10.1.40.13"

from urllib import urlencode
import requests
import ssl
import sys

ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()


def get_reource_type(res_id):
    global os_ip
    global ping_ip
    global phy_res_id
    global res_name
    global class_code

    os_data = {"apikey": apikey, "id": res_id}
    os_request_data = urlencode(os_data)
    os_url = base_url + "store/openapi/v2/resources/get?" + os_request_data
    print(os_url)
    os_response = requests.get(os_url, verify=False)
    print(os_response.content)
    os_content = os_response.json()
    if os_response.status_code != 200:
        print(os_content)
    check_relation = 'true'
    if os_content["classCode"] not in ["VM", "PCServer"]:
        res_name = os_content["name"]
        phy_url = "store/openapi/v2/resources/query_related?"
        phy_data = {"apikey": apikey}
        phy_request_data = urlencode(phy_data)
        phy_whole_url = base_url + phy_url + phy_request_data

        phy_headers = {'resource_id': res_id,
                       'Content-Type': 'application/json'}
        phy_condition = [{"field": "classCode", "operator": "IN",
                          "value": ['VM', 'PCServer', 'MiniServer']}]
        phy_body = {"conditions": phy_condition}
        try:
            print(phy_whole_url)
            print(phy_headers)
            print(phy_body)
            phy_response = requests.post(url=phy_whole_url, headers=phy_headers,
                                         json=phy_body, verify=False)
            phy_content = phy_response.json()
            print(phy_content)
            phy_class_code_result = phy_content["dataList"][0]["classCode"]
            phy_res_id = phy_content["dataList"][0]["id"]
            os_ip = os_content["ip"]
            ping_ip = vm_exector_ip
            class_code = phy_class_code_result
            return os_ip, phy_res_id, phy_class_code_result, ping_ip, class_code
        except Exception as e:
            print(e)
            check_relation = 'false'
            return
    elif os_content["classCode"] in ["VM", "PCServer"]:
        os_class_code = os_content["classCode"]
        os_res_id = os_content["id"]
        phy_res_id = os_res_id
        ping_ip = vm_exector_ip
        class_code = os_class_code
        return os_ip, phy_res_id, os_class_code, ping_ip, class_code


get_reource_type("5ef01dc20381fd37821100bc")


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
        print(response.json())
        for d in response.json():
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
        if response.json() == []:
            print(444)
            get_ipmi_result = "采控代理失联"
    except Exception as e:
        print(555)
        get_ipmi_result = "采控代理失联"
        print(e)
    return get_ipmi_result


def check_vm_phy(check_relation, class_code):
    global result
    if check_relation == 'false':
        result = "代理失联"
    else:
        if class_code == 'VM':
            result = "主机宕机"
        elif class_code == 'PCServer':
            result = "物理机"
    return result



