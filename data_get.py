#!/usr/bin/env python
import serial, threading, sys
from sys import stdout
from time import sleep
from xbee import XBee, ZigBee
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, send, emit

import numpy
import math
import random

# Set this var to "threading", "eventlet", or "gevent" to test the different
# async modes, or leave it set to None for app to choose best option based on
# installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

connected = False

# turn the flask app into socketio app
socketio = SocketIO(app, async_mode=async_mode, logger=True,
    engineio_logger=True)

if connected:
  xbee=serial.Serial(port='ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
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

  @socketio.on('connect', namespace='/test')
  def do():
    # visibility of global thread object??
    global thread
    socketio.emit('broadcast', {'newnum': 0}, namespace='/test')
    socketio.emit('ping_me', namespace='/test')

  @socketio.on('pong_me', namespace='/test')
  def dooo():
    try:
      thread.run()
      while (True):
        if (thread.packetAccepted):
          #Print values to stdout, write to file
          value = round(float(thread.albedoValue) / 100, 2)
          # Send value via websocket
          socketio.emit('broadcast', {'newnum': value}, namespace='/test')
          socketio.sleep(0.02)
          thread.packetAccepted = False
          thread.RX
    except:
      thread.stop()
      sleep(0.5)
      sys.exit()
else:

  class serialThread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      self.RUN_THREAD = True
      self.albedoValue = 0
      self.count = 0
      self.packetAccepted = True

    def stop(self):
      self.RUN_THREAD = False

    def run(self):
      # Parse the data
      self.count += (1/(12 * math.pi))
      value = 0.25 * math.cos(self.count) + 0.45
      value += 0.10 * math.cos(self.count*6)
      value += 0.01 * numpy.random.randn()
      value *= 100

      if (value < 0):
        value *= -1

      self.albedoValue = value
      sleep(0.01)

  @socketio.on('connect', namespace='/test')
  def do():
    # visibility of global thread object??
    global thread
    socketio.emit('broadcast', {'newnum': 0}, namespace='/test')
    socketio.emit('ping_me', namespace='/test')

  @socketio.on('pong_me', namespace='/test')
  def dooo():
    try:
      while (True):
        thread.run()
        if (thread.packetAccepted):
          #Print values to stdout, write to file
          value = round(float(thread.albedoValue) / 100, 2)
          # Send value via websocket
          socketio.emit('broadcast', {'newnum': value}, namespace='/test')
          socketio.sleep(0.02)
          thread.packetAccepted = False
        else:
          value = round(float(thread.albedoValue) / 100, 2)
          thread.packetAccepted = True
          socketio.sleep(0.1)
    except:
      thread.stop()
      sleep(0.5)
      sys.exit()

@app.route('/')
def index():
  # Send this page first so that client will be connected to socketio instance
  return render_template('index.html', async_mode=socketio.async_mode)

if __name__ == '__main__':
  # start thread
  thread = serialThread()
  thread.start()
  socketio.run(app, host='0.0.0.0', port=4567, debug=True)

