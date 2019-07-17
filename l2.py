#!/usr/bin/env python3
  
import ipaddress
import subprocess
from l1 import check_ip_1 as checkip

'''
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. 
Меняться должен только последний октет каждого адреса. 
По результатам проверки должно выводиться соответствующее сообщение.
'''

start = ipaddress.IPv4Address('192.168.1.1')
end = ipaddress.IPv4Address('192.168.1.3')

iplist = []
tmp = start

while tmp != end:
  iplist.append(str(tmp))
  tmp += 1

print(checkip(iplist))
