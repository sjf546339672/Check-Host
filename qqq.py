# coding: utf-8
import json
import os
import urllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests


def test_create_alert(url):
    """获取创建告警"""
    data = {
        "severity": 3,
        "name": "system.mem.pct_usage-CPU利用率",
        "description": "内存使用率超过80%",
        "occur_time": 1490251916807,
        "entity_name": "PC Server",
        "entity_addr": "10.2.1.2",
        "merge_key": "entity_name,name",
        "identify_key": "entity_name,entity_addr",
        "properties": [
            {
                "val": "dataCenter_A",
                "code": "location",
                "name": "Location"
            }
        ]
    }
    request = Request(url, data=data)
    response = urlopen(request)
    # response = requests.post(url, data=json.dumps(data), headers=headers)
    # print(response.status_code)
    # print(response.content)


# test_create_alert("http://10.1.200.204/alert/openapi/v2/create?apikey=e10adc3949ba59abbe56e057f2gg88dd&app_key=cnwzngxj2ha2ymsb55v07ujvd2p2dzdx")


def get_alert(id):
    base_url = "http://10.1.61.237/alert/openapi/v2/incident/query?"
    data = {
        "apikey": "e10adc3949ba59abbe56e057f20f88dd",
        "id": id,
        "pageSize": 10
    }
    requests_data = urlencode(data)
    url = base_url + requests_data
    print(url)
    response = requests.get(url)
    print(response.status_code)
    print(response.json())


# get_alert("5e781ad9142c200394594804")
# get_alert("0026c70528fe43f9b6885c42eebe5120")


def test_store(url):
    """资源库  查询资源类型列表"""
    response = requests.get(url)
    print(response.status_code)
    content = response.json()
    for i in content['dataList']:
        print(i)


# test_store("http://10.1.200.204/store/openapi/v2/models/classes/query?apikey=e10adc3949ba59abbe56e057f2gg88dd&page_size=-1")


def find_resource_types(res_id):
    """根据ID获取对应的资源对象详情"""
    base_url = "http://10.1.200.204/store/openapi/v2/resources/get?"
    data = {
        "apikey": "e10adc3949ba59abbe56e057f20f88dd",
        "id": res_id
    }
    request_data = urlencode(data)
    url = base_url + request_data
    response = requests.get(url)
    print(response.status_code)
    print(response.json())


# find_resource_types("5c493bd236fc22a42f97453f")
# find_resource_types("5c493bd236fc22a42f974570")

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Cookie": "language=zh_CN; auto_origin_referer=http://devops.uyunsoft.cn/#/automation; token=82f9ffef6d67785846a6374b9b27af42406a6d1fbc51798227d42ba8c494d51a; JSESSIONID=node01kqmo63r9ui3yvucyoq3g8rd450526.node0",
    "Host": "devops.uyunsoft.cn",
    "Pragma": "no-cache",
    "Referer": "http://devops.uyunsoft.cn/cmdb/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


