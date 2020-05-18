# coding: utf-8
# import json
# from urllib import urlencode
# from urlparse import urljoin
# import requests
#
# condition = [{"field": "classCode", "operator": "IN", "value": ['VM', 'PCServer', 'MiniServer']}]
#
# data = {
#     "apikey": "e10adc3949ba59abbe56e057f20f88dd",
#     "resource_id": "5ebf917c2350a90cacbbcc9d",
# }
#
# headers = {"resOwner": None,
#            "resource_id": "5ebf917c2350a90cacbbcc9d",
#            "relation_type_code": "RunsOn",
#            "Content-Type": "application/json"}
#
# body = {"pageNum": None,
#         "pageSize": None,
#         "needCount": None,
#         "orderFields": None,
#         "conditions": None,
#         "requiredFields": None
#         }
#
# base_url = "http://10.1.240.109/store/openapi/v2/resources/query_related?"
# request_data = urlencode(data)
# url = base_url + request_data
# print(url)
#
# # headers = {
# #     "Cookie": "token=d4672fd690bafe70fe54d7bc0614c7059790a64067fe4556fce69f78195e8702",
# #     "Content-Type": "application/json;charset=utf-8",
# #     "resource_id": "5ebf917c2350a90cacbbcc9d",
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
# # }
#
# response = requests.post(url, headers=headers, data=json.dumps(body))
# print(response.status_code, response.content)
#
