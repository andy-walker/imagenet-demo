#!/bin/bash

# the tensorflow routines in the python script seem to leak memory, and will
# eventually fall over if run for long enough, so rather than track it down,
# let's just continuously shell the process over and over again .. like the professionals we are

while :
    do
        python3 download-and-classify.py
done