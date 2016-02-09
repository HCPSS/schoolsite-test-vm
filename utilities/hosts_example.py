#!/usr/bin/env python

import socket, fcntl, struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

ip = get_ip_address('eth1')
fp = open("/etc/apache2/sites-enabled/vhosts.conf")

for i, line in enumerate(fp):
    if "ServerName" in line:
        print line.replace("ServerName", ip).strip()
