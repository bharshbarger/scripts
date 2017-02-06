#automate running of sslscan (or basically anything else if you replace sslscan with whatevers in your path you wanna iterate)
#based on https://unix.stackexchange.com/questions/7011/how-to-loop-over-the-lines-of-a-file
#usage is ./sslscan.sh <inputfile>
#can pipe output wherever
#! /bin/bash
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing

while IFS= read -r line; do
    #set up a case here for cmdline switch?
    #sslscan "$line"
    #curl --get --insecure --proxy 127.0.0.1:8080 $line
    #enum4linux $line
    wait
done < "$1" 
