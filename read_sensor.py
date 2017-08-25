#!/usr/bin/env python

# Source code adapted from http://www.perrygeo.com/
#        raspberry-pi-real-time-sensor-plots-with-websocketd.html
# To run, use command $ sudo python read_sensor.py
 
import RPi.GPIO as GPIO, time, os 
from xbee import XBee, ZigBee
import time, os
import threading, sys
import numpy
import datetime
from sys import stdout
import serial
import math
import pprint
import random
import xbee_serial
from xbee_serial import serialThread
from time import sleep

# Establish serial connection
# TODO: find port name for Arduino. (for now, /dev/ttyACM0 is used)
# source of help: https://raspberrypi.stackexchange.com/questions/
#                 12246/why-does-usb-port-enumeration-change

def bars(x, scale=0.01):
    return "#" * int(scale * x)    

def stopAudio():
#    os.system('pkill mpg123 &')
    return

def playAudio(trackNumber):
#    if (trackNumber == 0):
#        os.system('mpg123 -q audio/windchimes.mp3 &')
#    elif (trackNumber == 1):
#        os.system('mpg123 -q audio/water-dripping.mp3 &')
#    else:
#        os.system('mpg123 -q audio/river.mp3 &')
    return
   
def to_unix_timestamp(ts):
    """
    Get the unix timestamp (seconds from Unix epoch) 
    from a datetime object
    """
    start = datetime.datetime(year=1970, month=1, day=1)
    diff = ts - start
    return diff.total_seconds()


if __name__ == "__main__":
    xbee_serial.xBeeThread = serialThread()
    xbee_serial.xBeeThread.daemon = True
    xbee_serial.xBeeThread.RX = True
    xbee_serial.xBeeThread.start()
    try:
        trackNumber = 0
        while (True):
            if (xbee_serial.xBeeThread.packetAccepted):
                reading = xbee_serial.XBeeThread.acceptedValue
                reading = round(reading, 2)
                
                n = datetime.datetime.now()
                timestamp = to_unix_timestamp(n)
                print(reading)
                # Flush the output to stdout after every reading to make sure 
                # output isn't buffered
                time.sleep(0.30)
                stdout.flush()

                xbee_serial.XBeeThread.packetAccepted = False
                xbee_serial.xBeeThread.RX = True

    except:
        xbee_serial.xBeeThread.stop()
        print "\nStopping Thread..."
        sleep(0.5)
        print "Exiting"
        sys.exit()
