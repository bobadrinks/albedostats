#!/bin/bash
# Runs the python script and redirects output to a file called log.txt
# Process runs in the background
#nice -20 python xbee_serial.py &
nice -20 python get_data.py &
