#!/bin/bash
#usage ./rdpScan.sh <file with one ip per line>
#todo: add command switches

while read line
do
  	#echo "$line"
	rdesktop "$line" -u <user> -p <pass> -d <domain>
done < "${1:-/dev/stdin}"
