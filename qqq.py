# coding: utf-8
import os
# def net_is_used(port,ip='127.0.0.1'):
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     try:
#         s.connect((ip,port))
#         s.shutdown(2)
#         print('%s:%d is used' % (ip,port))
#         return True
#     except:
#         print('%s:%d is unused' % (ip,port))
#         return False
import socket


def check_prot(ip_addr, port):
    """检测ip上的端口是否开放"""
    socket_content = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_content.connect((ip_addr, port))
        socket_content.shutdown(2)
        print("{} is open".format(port))
        return True
    except Exception as e:
        print("{} is close".format(port))
        return False


print(check_prot("127.0.0.1", "6379"))  #



