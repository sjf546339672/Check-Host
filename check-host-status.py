# coding: utf-8
import json
import urllib

import os
import requests


def start(id, res_id):
    request_data = {
        "apikey": "e10adc3949ba59abbe56e057f2gg88dd",
        "pageSize": "10",
        "id": id
    }
    data = urllib.urlencode(request_data)
    alert_url = "http://10.1.61.237/alert/openapi/v2/incident/query?"+data
    get_number = get_alert_number(alert_url)
    print(get_number)
    if get_number <= 50:
        pass


def get_alert_number(url):
    """获取告警的数量"""
    response = requests.get(url)
    data = response.json()
    get_number = data["records"][0]["count"]
    return get_number


def ping_ip(ip_addr):
    result = os.popen('ping -n 1 ' + ip_addr, 'r')
    shuchu = result.read()
    result.close()
    if not shuchu.count('请求超时'):
        return True
    else:
        return False


def main():
    id = "0026c70528fe43f9b6885c42eebe5120"
    start(id, 2222)


if __name__ == '__main__':
    main()











"""
{
	"severity":       3, # 
	"name":           "testalert",
	"description":    "内存使用率超过80%", # 
	"occur_time":     1490251916807,
	"entity_name":    "PC Server",
	"entity_addr":    "10.2.1.2",
	"merge_key":      "testalert, PC Server",
	"identify_key":   "PC Server, 10.2.1.2", 
	"type":           "metric",
	"properties":     [
		{
			"val": "测试使用alert",
			"code": "metricname",
			"name":	"METRIC_NAME"
		}
	]
}
"""



