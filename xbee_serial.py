#!/usr/bin/env python
import serial, threading, sys
from sys import stdout
from time import sleep

# Declare XBee
xbee=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
# Characters that start and end the packet of data
PACKET_START = '<'
PACKET_END = '>'
# Store albedo value in this variable
albedoValue = 0

# Parse data from the XBee by reading in a loop
while True:
  # Read the next line sent by the XBee, in a loop
  newLine = xbee.readline()

  # Make sure that the line that was read isn't empty, and then
  # check if the first char is a '<' start char and the char that ended the last
  # packet was a '>' end char
  if (newLine != '' and newLine[0] == PACKET_START and newLine[-2] == PACKET_END):
    # Now parse the actual packet
    newLine = newLine.strip(PACKET_START);
    newLine = newLine.strip(PACKET_END);

    # Populate the values list with the transmitted numbers
    values = newLine.split('|')
    if len(values) >= 2:
      # Make sure that the two numbers are the same; if they're not, something
      # went wrong and this data packet is corrupted/invalid
      if (values[0] == values[1]):

        # No errors detected while parsing; this albedo value is accepted
        albedoValue = int(values[0])

        # Print values to stdout, write to file (script will read from log file
        # and update webpage
        print(float(albedoValue) / 100)
        stdout.flush()

sleep(0.5)
sys.exit()
