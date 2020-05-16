# coding: utf-8
import json
from urllib.parse import urlencode
from urllib.request import urlopen
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
        "apikey": "e10adc3949ba59abbe56e057f2gg88dd",
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
        return resource_name
    except Exception as e:
        print(e)


def main(alert_id, res_id):
    get_number = get_alert_number(alert_id)
    if get_number <= 50:
        resource_name = get_reource_type(res_id)
        if resource_name == "虚拟机":
            ip = '10.1.100.12'
        else:
            ip = '10.1.100.14'


if __name__ == '__main__':
    alert_id = "5ebf971844d9e79b29ab4039"
    res_id = "5e5f4347438042e42641a5d1"
    main(alert_id, res_id)



