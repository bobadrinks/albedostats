#!/bin/sh
sudo nice -20 python read_sensor.py > log.txt &

websocketd --port 8000 --staticdir=./static --sameorigin=true tail -f log.txt
# websocketd --port 8000 --devconsole --sameorigin=true tail -f log.txt
