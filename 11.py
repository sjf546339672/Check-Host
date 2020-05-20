# coding: utf-8
import json
from urllib import urlencode

import requests

base_url = "http://10.1.240.109/"
alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"
alert_apikey = "9cc4871e46094635a19d26557f9bb7f4"


def check_result(result_ping, result_ssh, result_impi):
    """检查结果"""
    if result_ping == 0:
        if result_ssh == 0:
            return "采控代理异常"
        else:
            return "HANG住了"
    else:
        if result_impi == 0:
            return "网络不可达"
        else:
            return "主机宕机"


def alert_relate(parentId, child):
    """创建父子告警关联"""
    # alert13 = "06b7742634d0eea11c3d614ccd676b80"
    # alert3 = "193fe81c529f4391c9610f548fe765bc"
    data = {"apikey": apikey}

    body = {
        "parentId": parentId,
        "childs": [child]
    }
    request_data = urlencode(data)
    url = "http://10.1.240.109/" + "alert/openapi/v2/incident/merge?" + request_data
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    try:
        response = requests.post(url=url, json=body, headers=headers)
        print(response.status_code, response.content)
    except Exception as e:
        return


def get_result_alert(result_ping, result_ssh, result_impi):
    """创建一个新的告警"""
    data = {"apikey": apikey, "id": alert_id}
    request_data = urlencode(data)
    url = base_url + "alert/openapi/v2/incident/query?" + request_data
    response = requests.get(url)
    app_key = response.json()["records"][0]["appKey"]
    parentid = response.json()["records"][0]["id"]

    result = check_result(result_ping, result_ssh, result_impi)
    print(result)

    create_data = {"apikey": alert_apikey, "app_key": app_key}
    create_body = {
        "severity": 2,
        "name": result,
        "description": result,
        "entity_name": "10.1.1.1",
        "entity_addr": "10.1.62.106"
    }
    create_request_data = urlencode(create_data)
    create_url = base_url + "alert/openapi/v2/create?" + create_request_data
    print(create_url)
    headers = {"Content-Type": "application/json;charset=utf-8"}
    try:
        requests.post(url, json=create_body, headers=headers)
    except Exception as e:
        return

    alert_relate(parentid, child)


get_result_alert(0, 0, 0)



"""
{
	"severity": 2,
	"name": "HANG住了",
	"description": "HANG住了",
	"entity_name": "10.1.1.1",
	"entity_addr": "10.1.62.172"
}
"""