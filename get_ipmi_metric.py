#!/usr/bin/env python
# coding: UTF-8
# Author: zhengyd@uyunsoft.cn
# Date  : 2020/5/17

import json
import requests
from urlparse import urljoin


class UYunApi(object):
    def __init__(self, base_url, apikey, timeout=10):
        self.base_url = base_url
        self.apikey = apikey
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json",
                        "apikey": self.apikey,
                        'Cache-Control': 'no-cache'
                        }

    def fetch(self, url, method='GET', **kwargs):
        url = urljoin(self.base_url, url)
        headers = kwargs.pop('headers') if kwargs.get('headers') else self.headers
        if kwargs.get('params'):
            kwargs['params'].update({'apikey': self.apikey})
        else:
            kwargs['params'] = {'apikey': self.apikey}
        print(headers)
        print(url)
        print(kwargs)
        print(method)
        try:
            resp = requests.request(method, url, headers=headers, timeout=self.timeout, **kwargs)
            if resp.status_code >= 400:
                raise Exception('{} {}, status_code: {}, return {}'.format(method, resp.url, resp.status_code, resp.text))
            if resp.content:
                result = json.loads(resp.content)
                return result
            else:
                print resp.status_code, resp.url
        except Exception as e:
            print(e)

    def res_get_by_id(self, res_id):
        params = {'id': res_id}
        return self.fetch('store/openapi/v2/resources/get', params=params)

    # 根据关系查询资源
    def res_queryRelatedResources(self, resource_id, relation_type_code, conditions=None, requiredFields=None,
                              orderFields=None, pageNum=None, pageSize=None, needCount=None, res_owner=None):
        url = urljoin(self.base_url, 'store/openapi/v2/resources/query_related')
        headers = {"resOwner": res_owner,
                   "resource_id": resource_id,
                   "relation_type_code": relation_type_code,
                   "Content-Type": "application/json"}
        data = {"pageNum": pageNum,
                "pageSize": pageSize,
                "needCount": needCount,
                "orderFields": orderFields,
                "conditions": conditions,
                "requiredFields": requiredFields
                }
        # print data
        return self.fetch(url, 'POST', data=json.dumps(data), headers=headers)

    def datapoints_query_last(self, object_ids):
        if isinstance(object_ids, (list, tuple)):
            object_ids = ','.join(object_ids)
        params = {'tag': 'object:{}'.format(object_ids)}
        return self.fetch('/store/openapi/v2/datapoints/query_last', params=params)

    def datapoints_query_by_res_id(self, metric_query_by_res_id):
        params = {'resId': metric_query_by_res_id}
        return self.fetch('store/openapi/v2/datapoints/queryByResId', params=params)

    def metric_query(self):
        return self.fetch('store/openapi/v2/models/metrics/query')

    def datapoints_query(self, metric, tags):
        data = {
            "metric": metric,
            "tags": tags,
            "time": {
                "interval": 1000,
                "interval_unit": "seconds",
                "aggregator": "last"
            },
            "group_by": {
                "tag_keys": ["ip"]
            },
            "is_use_cached": False
        }
        return self.fetch('/store/openapi/v2/datapoints/query', 'POST', data=json.dumps(data))


if __name__ == '__main__':
    url = "http://10.1.5.250/"
    # url = "http://10.1.240.109"
    # url = "http://10.1.61.237/"
    apikey = "e10adc3949ba59abbe56e057f2gg88dd"
    uyun = UYunApi(url, apikey)

    # res_id = '5ea7831622908172cd8f625e'
    # res_id = '5e8d7f7a547d4efbd0247858'
    res_id = '5ea146be2290815a80c6ac21'
    # res_id = '5e81a3a9547d4e33e00c81c1'
    # res_id = '5df8f5c28ad899599668ed00'

    # res_id = "5e85a2d82350a94b818db72e"

    # print uyun.res_get_by_id(res_id)
    # print uyun.datapoints_query_by_res_id(res_id)

    # m = 'system.tcp.established'
    m = 'system.tcp.syn_sent'
    # m = "ipmi.chassis.power.status"
    datas = uyun.datapoints_query_last(res_id)
    # print(datas)
    for d in datas:
        if d['metric'] == m:
            print ("=========>>>", m, d['value'], type(d['value']))
    # print uyun.metric_query()
    # print uyun.datapoints_query('system.io.await', {'ip': '10.1.5.76'})
    # print uyun.datapoints_query(m, {'object': res_id})
    #
    # condition = [{"field": "classCode", "operator": "IN", "value": ['VM', 'PCServer', 'MiniServer']}]
    # print uyun.res_queryRelatedResources(res_id, 'RunsOn', condition)
    # print uyun.res_queryRelatedResources(res_id, )