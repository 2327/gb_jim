#!/usr/bin/env python3

import ipaddress
import subprocess

iplist = ["127.0.0.1", "8.8.8.8", "geekbrains.ru"]
def check_ip_0(iplist):
    for ip in iplist:
        try:
            subprocess.check_output(["ping", "-c", "1", ip])
            print(f"{ip} Узел доступен")
        except subprocess.CalledProcessError:
            print(f"{ip} Узел не доступен")

def check_ip_1(iplist):
    for ip in iplist:
        p = subprocess.Popen("ping -c1 "+ip, shell=True, stdout=subprocess.PIPE)
        p.wait()
        if p.poll():
            print(f"{ip} Узел не доступен")
        else:
            print(f"{ip} Узел доступен")

check_ip_0(iplist)
