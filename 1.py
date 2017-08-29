#!/usr/bin/env python

import serial, threading, sys
from sys import stdout
from time import sleep
xbee=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
PACKET_START = '<'
PACKET_END = '>'

class serialThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.PACKET_SIZE = 15
    self.NUM_TXs = 5
    self.BUFFER_SIZE = (self.PACKET_SIZE * self.NUM_TXs)
    self.NEW_PACKET = False
    self.rxBuffer = ""
    self.RX = True
    self.RUN_THREAD = True
    self.packetAccepted = False
    self.albedoValue = 0

  def stop(self):
    self.RUN_THREAD = False

  def run(self):
    # Parse the data
    while (self.RUN_THREAD):
      if (self.RX == True):
        rxStarted = False

        while (self.NEW_PACKET == False and self.RUN_THREAD):
          newChar = xbee.read()
          sleep(0.01)
          if (rxStarted):
            if (newChar != PACKET_END):
              self.rxBuffer += newChar
              rxStarted = False
              if (len(self.rxBuffer) >= self.BUFFER_SIZE):
                self.rxBuffer = ""
              else:
                self.NEW_PACKET = True
      elif (newChar == PACKET_START):
        rxStarted = True

    values = self.rxBuffer.split('|')
    if len(values) >= 2:
      if (values[0] == values[1]):
        self.albedoValue = int(values[0])
        self.RX = False
        self.packetAccepted = True
    self.NEW_PACKET = False
    self.rxBuffer = ""

xBeeThread = serialThread()
xBeeThread.daemon = True
xBeeThread.RX = True
xBeeThread.start()
try:
  while True:
    if xBeeThread.packetAccepted:
      # write vals to file
      #logFile.write(str(float(xBeeThread.albedoValue) / 100) + "\n");
      print(float(xBeeThread.albedoValue)/100)
      xBeeThread.packetAccepted = False
      xBeeThread.RX = True
      #logFile.flush()
      stdout.flush()

except:
  xBeeThread.stop()
  logFile.close()
  sleep(0.5)
  sys.exit()
