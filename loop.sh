#automate running of sslscan (or basically anything else if you replace sslscan with whatevers in your path you wanna iterate)
#based on https://unix.stackexchange.com/questions/7011/how-to-loop-over-the-lines-of-a-file
#usage is ./sslscan.sh <inputfile>
#can pipe output wherever
#! /bin/bash
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing

while IFS= read -r line; do
    #set up a case here for cmdline switch?
    
    #sslscan an ip
    #sslscan "$line"
    
    #curl an ip 
    #curl --get --insecure --proxy 127.0.0.1:8080 $line
    
    #run enum4linux
    #enum4linux $line
    
    #test for tcp timestamps
    #hping3 -S -c 2 $line -p 445 --tcp-timestamp
    
    #Responder's RunFinger.py with greppable output
    #./RunFinger.py -g -i $line
    
    wait
done < "$1" 
