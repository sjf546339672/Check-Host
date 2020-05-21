# coding: utf-8
from urllib import urlencode

import requests

base_url = "http://10.1.240.109/"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"
vm_exector_ip = "10.1.100.213"
pc_exector_ip = "10.1.100.213"


def get_reource_type(res_id):
    """获取资源参数"""
    # 入参 res_id, apikey
    # 出参 os_ip phy_ip  phy_res_id
    global os_ip
    global ping_ip
    global phy_res_id
    os_data = {"apikey": apikey, "id": res_id}
    os_request_data = urlencode(os_data)
    os_url = base_url + "store/openapi/v2/resources/get?" + os_request_data
    os_response = requests.get(os_url)
    os_content = os_response.json()
    if os_content["classCode"] not in ["VM", "PCServer"]:
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


print get_reource_type("5ebf917c2350a90cacbbcc9d")  #



