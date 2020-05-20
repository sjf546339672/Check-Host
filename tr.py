# coding: utf-8
import json
from urllib import urlencode

import requests


def get_result_alert():
    """创建一个新的告警"""
    apikey = "9cc4871e46094635a19d26557f9bb7f4"
    data = {
        "apikey": apikey,
        "app_key": "a8g645w6wdb99ovziohny5kf7ocekhbn"
    }
    body = {
        "severity": 3,
        "name": "testalert",
        "description": "Alert",
        "entity_name": "10.1.1.1",
    }
    request_data = urlencode(data)
    get_url = 'alert/openapi/v2/create?'
    url = "http://10.1.240.109/" + get_url + request_data
    try:
        response = requests.post(url, data=json.dumps(body))
        print(url)
        print(response.status_code)
        print(response.content)
    except Exception as e:
        return


get_result_alert()

