# coding: UTF-8
import json
from urlparse import urljoin

import requests
# from urlparse import urljoin


class StoreApi(object):
    """
    统一资源库 openapi 接口，详细使用方法查看kb API 文档
    http://www.uyunsoft.cn/kb/display/productrelease/Pacific+Open+API
    """
    def __init__(self, base_url, apikey, debug=False):
        self.debug = debug
        self.apikey = apikey
        self.base_url = urljoin(base_url, 'store/openapi/v2/')
        self.params = {"apikey": self.apikey}
        self.headers = {"Content-Type": "application/json"}

    # 封装request 执行器，返回列表
    def do_request(self, method, url, data=None, headers=None, params=None, **kwargs):
        result = []
        if not headers:
            headers = self.headers
        if not params:
            params = self.params
        if isinstance(data, dict):
            data = json.dumps(data)
        try:
            r = requests.request(method, url, data=data, headers=headers, params=params, **kwargs)
            if self.debug:
                print("\n---------------------------------------")
                print("Debug: ")
                print("url: ", url)
                print("status_code:",  r.status_code)
                print("headers", headers)
                print("data:", data)
                print("params:", params)
                print(r.content)
                print("---------------------------------------")
            if r.status_code == 200:
                if r.content:
                    content = json.loads(r.content)
                    # result = content
                    if isinstance(content, dict):
                        result = content.get('dataList')
                    elif isinstance(content, list):
                        result = content
            else:
                print("请求出错:", url)
                print(r.status_code, r.content)
        except Exception as err:
            print("网络请求失败，请检查URL或代理是否正常")
            print(url)
            print(err)
        return result

    # 查询符合条件的资源
    def queryResObjects(self, conditions=None, requiredFields=None, orderFields=None, pageNum=None,
                        pageSize=None, needCount=None, res_owner=None):

        url = urljoin(self.base_url, 'resources/query')
        headers = {"resOwner": res_owner, "Content-Type": "application/json"}
        data = {"pageNum": pageNum,
                "pageSize": pageSize,
                "needCount": needCount,
                "orderFields": orderFields,
                "conditions": conditions,
                "requiredFields": requiredFields
                }
        # print json.dumps(data, indent=2)
        return self.do_request('POST', url, data=data, headers=headers)

    # 根据关系查询资源
    def queryRelatedResources(self, resource_id, relation_type_code, conditions=None, requiredFields=None,
                              orderFields=None, pageNum=None, pageSize=None, needCount=None, res_owner=None):
        url = urljoin(self.base_url, 'resources/query_related')
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
        return self.do_request('POST', url, data=data, headers=headers)

    # 获取所有分层
    def getAllResLayer(self):
        url = urljoin(self.base_url, 'models/classes/layers/get_all')
        return self.do_request('GET', url)

    # 根据编码加载资源类型，获取对应的资源类型详情
    def getResClass(self, code, required_fields=None):
        url = urljoin(self.base_url, 'models/classes/get')
        params = {"apikey": self.apikey,
                  "code": code,
                  "required_fields": required_fields
                  }
        return self.do_request('GET', url, params=params)

    # 获取类型树：将满足条件的类型，按类型分层进行分组
    def getResClassTree(self, layer_code=None, class_name=None, required_fields=None, res_owner=None):
        url = urljoin(self.base_url, 'models/classes/assemble')
        params = {"apikey": self.apikey,
                  "layer_code": layer_code,
                  "class_name": class_name,
                  "required_fields": required_fields,
                  "res_owner": res_owner
                  }
        return self.do_request('GET', url, params=params)

    # 根据关键属性获取对应的资源类型详情
    def getResObjectByKeyAttrs(self, class_code=None, attrs=None, required_fields=None):
        url = urljoin(self.base_url, 'resources/get_by_keyattrs')
        params = {"apikey": self.apikey,
                  "class_code": class_code,
                  "attrs": attrs,
                  "required_fields": required_fields,
                  }
        return self.do_request('GET', url, params=params)

    # 更新一个资源，只能更新动态属性，不能更新固有属性。为了定位待更新的资源，ID或关键属性必须提供一个。
    def updateResObject(self, id, tenantId, classCode, className=None, sources=None, tags=None, resOwners=None, createTime=None, updateTime=None):
        url = urljoin(self.base_url, 'resources/get_by_keyattrs')
        data = {"id": id,
                "tenantId": tenantId,
                "classCode": classCode,
                "className": className,
                "sources": sources,
                "tags": tags,
                "resOwners": resOwners,
                "createTime": createTime,
                "updateTime": updateTime
                }
        return self.do_request('POST', url, data=data)

    # 获取指定资源上所打的标签
    def getResourceTag(self, resource_id, res_owner=None):
        url = urljoin(self.base_url, 'resources/tags/get')
        params = {"apikey": self.apikey,
                  "resource_id": resource_id,
                  "res_owner": res_owner}
        return self.do_request('GET', url, params=params)

    # 将标签打到指定的资源上
    def addResourceTag(self, resource_id, res_owner, tag):
        url = urljoin(self.base_url, 'resources/tags/add')
        headers = {"res_owner": res_owner,
                   "resource_id": resource_id,
                   "Content-Type": "application/json"}
        return self.do_request('POST', url, data=tag, headers=headers)

    def saveResObject(self, data):
        url = urljoin(self.base_url, 'resources/save')
        return self.do_request('POST', url, data)
