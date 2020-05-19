# coding: utf-8
from urllib import urlencode

import requests

# result_ping  result_ssh  result_impi


# def test(result_ping, result_ssh, result_impi):
#     if result_ping is True:
#         if result_ssh is True:
#             return "采控代理异常"
#         else:
#             return "HANG住了"
#     else:
#         if result_impi is True:
#             return "网络不可达"
#         else:
#             return "主机宕机"

# base_url = "http://10.1.5.250/"
# base_url = "http://10.1.240.109/"
# url = "store/openapi/v2/datapoints/query_last?"
# data = {
#     'apikey': 'e10adc3949ba59abbe56e057f2gg88dd',
#     # 'tag': 'object:5ea146be2290815a80c6ac21'
#     'tag': 'object:5ebf917d2350a90cacbbcca1'
# }
# request_data = urlencode(data)
# whole_url = base_url+url + request_data
# headers = {'apikey': 'e10adc3949ba59abbe56e057f2gg88dd', 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
#
# response = requests.get(url=whole_url, headers=headers)
# print(response.status_code, response.content)


def mySqrt(x):
    """
    :type x: int
    :rtype: int
    """
    t = 1
    while t*t <= x:
        t += 1
    return t - 1


print mySqrt(0)