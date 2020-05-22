# coding: utf-8
import json
from urllib import urlencode
import requests

base_url = "http://10.1.240.109/"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"


def check_ipmi(res_id):
    """检查主机是否上电"""
    global get_ipmi_result
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
        response = requests.get(url=whole_url, headers=headers)
        for d in response.json():
            if d['metric'] == m:
                if str(d['value']) == "1.0":
                    get_ipmi_result = "true"
                elif str(d['value']) == "0.0":
                    get_ipmi_result = "false"
        get_ipmi_result = "true"
        return get_ipmi_result
    except Exception as e:
        print("检查是否失败")


print check_ipmi("5ebf917c2350a90cacbbcc9d")