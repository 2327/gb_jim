#!/usr/bin/env python3
  
import ipaddress
import subprocess
#from l1 import check_ip_1 as checkip

start = ipaddress.IPv4Address('192.168.1.1')
end = ipaddress.IPv4Address('192.168.1.3')
iplist = []
tmp = start

def check_ip(iplist):
  for ip in iplist:
    p = subprocess.Popen("ping -c1 " + ip, shell=True, stdout=subprocess.PIPE)
    p.wait()
    if p.poll():
      print(f"{ip} Узел не доступен")
    else:
      print(f"{ip} Узел доступен")

while tmp != end:
  iplist.append(str(tmp))
  tmp += 1

print(iplist)
print(check_ip(iplist))
