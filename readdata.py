import serial

# set up serial connection speed
ser = serial.Serial('/dev/ttyACM0', 9600)

# main loop
while 1:

    #receive data from Arduino
    response = ser.readline()

    print(response.decode().strip())
