#!/usr/bin/env python
import serial, threading, sys
from sys import stdout
from time import sleep
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line

define("port", default=8000, help="run on the given port", type=int)

# Store clients in dictionary
clients = dict()

xbee=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
PACKET_START = '<'
PACKET_END = '>'
logFile = open("log.txt", "w", 0)

class IndexHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self):
    # self.write("This is your response")
    self.render("index.html")
    self.finish()

# See https://media.readthedocs.org/pdf/tornado/latest/tornado.pdf
# for tornado websocket documentation
class WebSocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    self.id = self.get_argument("Id")
    self.stream.set_nodelay(True)
    clients[self.id] = {"id": self.id, "object": self}

  def on_message(self, message):
    self.write_message("You said: " + message)

  def on_close(self):
    if self.id in clients:
      del clients[self.id]
    print("Websocket closed")

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

xBeeThread = serialThread()
xBeeThread.daemon = True
xBeeThread.RX = True
xBeeThread.start()
try:
  while (True):
    if (xBeeThread.packetAccepted):
      #Print values to stdout, write to file
      value = float(xBeeThread.acceptedValue) / 100
      # Write the value to file
      logFile.write(str(value) + "\n")
      # write_message(value, False)
      xBeeThread.packetAccepted = False
      xBeeThread.RX = True
#      stdout.flush()
    else:
      #print(0)
      logFile.write(str(0) + "\n")
      logFile.flush()
      sleep(0.1)
except:
  xBeeThread.stop()
  logFile.close()
  sleep(0.5)
  sys.exit()

app = tornado.web.Application([
  (r'/', IndexHandler),
  (r'/', WebSocketHandler),
])
if __name__ == '__main__':
  parse_command_line()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
