# coding: utf-8
import json
from urllib import urlencode

import requests

base_url = "http://10.1.240.109/"
apikey = "e10adc3949ba59abbe56e057f2gg88dd"
# vm_exector_ip = "10.1.100.213"
# pc_exector_ip = "10.1.100.213"
# alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
alert_id = "6e7996ca6d4148178966c26b72aa4c03"
# res_id = "5ecb29c82350a90cacbbcd71"


def get_alert_number():
    """获取计算告警的数量"""
    request_data = {"apikey": apikey, "pageSize": "10",
                    "id": alert_id}
    data = urlencode(request_data)
    url = base_url + "alert/openapi/v2/incident/query?" + data
    try:
        response = requests.get(url)
        data = response.json()
        get_number = data["records"][0]["count"]
        return get_number
    except Exception as e:
        return


print(get_alert_number())