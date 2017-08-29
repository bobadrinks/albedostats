#!/usr/bin/env python
import serial, threading, sys
from sys import stdout
from time import sleep
from xbee import XBee, ZigBee
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

import numpy
import math
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# turn the flask app into socketio app
socketio = SocketIO(app)

connected = False
count = 0
logFile = open("log.txt", "w")

if connected:
  xbee=serial.Serial(port='ttyUSB0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
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
                if (len(self.rxBuffer) >= self.BUFFER_SIZE):
                  rxStarted = False
                  self.rxBuffer = ""
              else:
                rxStarted = False
                self.NEW_PACKET = True
        elif (newChar == PACKET_START):
          rxStarted = True

      values = self.rxBuffer.split('|')
      if len(values) >= 2:
        if (values[0] == values[1]):
          self.acceptedValue = int(values[0])
          self.RX = False
          self.packetAccepted = True
      self.NEW_PACKET = False
      self.rxBuffer = ""

else:
  while (True):
    count += (1/(12 * math.pi))
    value = 0.25 * math.cos(count) + 0.45
    value += 0.15 * math.cos(count*6)
    value += 0.1 * numpy.random.randn()
    if (value < 0):
      value *= -1
    socketio.emit('newnumber', {'number': value}, namespace='/')
#    logFile.write(str(value) + "\n")
#    logFile.flush()
    sleep(0.5)


@app.route('/')
def index():
  # Send this page first so that client will be connected to socketio instance
  return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
  # visibility of global thread object??
  global xBeeThread
  print('Client connected')

  # start thread
  if not xBeeThread.isAlive():
    xBeeThread = serialThread()
    xBeeThread.daemon = True
    xBeeThread.RX = True
    xBeeThread.start()
    try:
      while (True):
        if (xBeeThread.packetAccepted):
          #Print values to stdout, write to file
          value = float(xBeeThread.acceptedValue) / 100
          # Send value via websocket
          socketio.emit('newnumber', {'number': value}, namespace='/')
#        logFile.write(str(value) + "\n")
#        logFile.flush()
          xBeeThread.packetAccepted = False
          xBeeThread.RX = True
        else:
          logFile.write(str(value) + "\n")
          logFile.flush()
          sleep(0.1)
    except:
      xBeeThread.stop()
      sleep(0.5)
      sys.exit()


if __name__ == '__main__':
  socketio.run(app)

