# coding: utf-8
import requests
from urllib import urlencode

global ping_ip

def get_reource_type(vm_exector_ip):
    """获取资源参数"""
    os_data = {"apikey": apikey, "id": res_id}
    os_request_data = urlencode(os_data)
    os_url = base_url + "store/openapi/v2/resources/get?" + os_request_data
    os_response = requests.get(os_url, verify=False)
    os_content = os_response.json()
    os_ip = os_content["ip"]
    if os_content["classCode"] not in ["VM", "PCServer"]:
        phy_url = "store/openapi/v2/resources/query_related?"
        phy_data = {"apikey": apikey}
        phy_request_data = urlencode(phy_data)
        phy_whole_url = base_url + phy_url + phy_request_data

        phy_headers = {'resource_id': res_id,'Content-Type': 'application/json'}
        phy_condition = [{"field": "classCode", "operator": "IN", "value": ['VM', 'PCServer', 'MiniServer']}]
        phy_body = {"conditions": phy_condition}
        try:
            phy_response = requests.post(url=phy_whole_url, headers=phy_headers, json=phy_body, verify=False)
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







