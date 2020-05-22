# coding: utf-8
import json
from urllib import urlencode

import requests

base_url = "http://10.1.240.109/"
alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"
alert_apikey = "9cc4871e46094635a19d26557f9bb7f4"

from urllib import urlencode
import requests
import json


def check_result(result_ping, result_ssh, result_impi):
    """检查结果"""
    result_ping = json.loads(result_ping).values()[0]
    if result_ping == "true":
        result_ssh = json.loads(result_ssh).values()[0]
        if result_ssh == "true":
            return "采控代理异常"
        else:
            return "HANG住了"
    else:
        if result_impi == "true":
            return "网络不可达"
        else:
            return "主机宕机"


def create_new_alert(apikey, result_ping, result_ssh, result_impi, ip, app_key):
    """创建一个新的告警"""
    result = check_result(result_ping, result_ssh, result_impi)

    data = {"apikey": apikey, "app_key": app_key}
    body = {"severity": 3, "name": result, "description": result, "entity_name": ip}
    request_data = urlencode(data)
    get_url = 'alert/openapi/v2/create?'
    url = base_url + get_url + request_data
    try:
        response = requests.post(url, json=body)
        print(response.status_code)
    except Exception as e:
        print(e)


result_ping = json.dumps({'10.62.106': 'true'})
result_ssh = json.dumps({'10.62.106': 'true'})
result_impi = ""
ip = "10.1.62.106"
app_key = "a8g645w6wdb99ovziohny5kf7ocekhbn"


create_new_alert(apikey, result_ping, result_ssh, result_impi, ip, app_key)






