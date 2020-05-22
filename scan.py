#!/usr/bin/env python2
# coding: UTF-8
# UYUN Automation script
# @Author: zhengyd@uyunsoft.cn
# @Date  : 2019/2/27
import re
import platform
import socket
import sys
import time
import ipaddress
import psutil
from concurrent import futures
from subprocess import Popen, PIPE, STDOUT

socket.setdefaulttimeout(1)
IS_Windows = platform.system() == 'Windows'


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE,)
    stdout, _ = p.communicate()
    return p.returncode, stdout.strip()


def get_arp():
    """获取系统当前 arp 列表"""
    out = run_cmd('arp -a')[1]
    arp = {}
    for line in out.splitlines():
        ip = re.search(r'(\d+\.){3}\d+', line)
        mac = re.search(r'([\da-zA-Z]{2}[-:]){5}[\da-zA-Z]{2}', line)
        if ip and mac:
            arp[ip.group()] = mac.group()
    return arp


def ip_to_int(ip):
    """转换IPv4地址为整数"""
    return reduce(lambda a, b: a << 8 | b, map(int, ip.split(".")))


def int_to_ip(_int):
    """将整数转换为IPv4地址"""
    return ".".join(map(lambda n: str(_int >> n & 0xFF), [24, 16, 8, 0]))


def port_check(ip, port):
    """检查端口"""
    try:
        s = socket.socket()
        s.connect((ip, int(port)))
        s.close()
        print port, 'opened'
        return port
    except socket.error as e:
        return


def ping(ip_addr, echo_opened=True, echo_closed=False, num=1):
    """ping 测试"""
    is_open = False
    cmd = 'ping -{} {} {}'.format('n' if platform.system() in ['Windows', 'Darwin'] else 'c', num, ip_addr)
    code, out = run_cmd(cmd)
    # print out
    if re.search('ttl', out, re.I):
        is_open = True

    if is_open:
        if echo_opened:
            print '{:<15} opened'.format(ip_addr)
        return ip_addr
    else:
        if echo_closed:
            print '{:<15} closed'.format(ip_addr)


def scan_ports(ip, port_start=20, port_end=1024):
    open_ports = []
    threads = [executor.submit(port_check, ip, port) for port in range(int(port_start), int(port_end))]
    for t in threads:
        r = t.result()
        # print r
        if r:
            open_ports.append(r)
    print ip, open_ports


def scan_ips(ips, echo_opened=False, echo_closed=False, get_mac=True):
    print "开始扫描：", ips
    try:
        ips = [ipaddress.ip_address(unicode(ips))]
    except:
        try:
            ips = ipaddress.ip_network(unicode(ips)).hosts()
        except:
            print('输入的IP段格式不对')
            return []
    jobs = []
    for ip in ips:
        jobs.append(executor.submit(ping, str(ip), echo_opened, echo_closed))
    opened = []
    for job in jobs:
        open_ip = job.result()
        if open_ip:
            opened.append(open_ip)
    print "Open IP个数：", len(opened)
    if opened and get_mac:
        print "\nIP 和 MAC 对应表:"
        arps = get_arp()
        for i in sorted(opened, key=lambda _ip: ip_to_int(_ip)):
            print '{:<15}  {}'.format(i, arps.get(i))
    return opened


def main():
    result = {}
    ips = start_port = end_port = None
    if len(sys.argv) == 2:
        ips = sys.argv[1]
    elif len(sys.argv) == 4:
        ips, start_port, end_port = sys.argv[1:]
    else:
        ips = raw_input('请输入待扫描IP段, 格式：10.1.250.0/24: ') or '10.1.251.0/24'
        start_port = raw_input('输入启始端口:')
        end_port = raw_input('输入结束端口:')

    if start_port and end_port:
        print('扫描IP和端口')
        open_ips = scan_ips(ips)
        for ip in open_ips:
            scan_ports(ip, start_port, end_port)
    else:
        scan_ips(ips)


if __name__ == '__main__':
    start = time.time()
    executor = futures.ThreadPoolExecutor(max_workers=200)
    main()
    print '总耗时：', int(time.time() - start), 's'