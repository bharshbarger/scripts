#!/usr/bin/env python

#todo: randomize srcip/port/payload
#crate send loop with rate control

from scapy.all import *

srcIp = '192.168.222.222'
dstIp = '127.0.0.1'
srcPort = '22222'
dstPort = '33333'

payload = 'payload here'


#TCP
#send(IP(src=srcIp, dst=dstIp) / TCP(sport=srcPort, dport=dstPort) / payload )


#ICMP
send(IP(src="10.0.99.100",dst="127.0.0.1")/ICMP()/"Hello World")
