This project uses analog sensors with a Raspberry Pi, logs and streams those values via websocketd and, finally, plots the data in a real time HTML/JS interface (smoothie-js).

This is the blog/project on which this project was based:
[https://perrygeo.com/raspberry-pi-real-time-sensor-plots-with-websocketd.html](https://perrygeo.com/raspberry-pi-real-time-sensor-plots-with-websocketd.html)

To Run:
From the command-line, use the following command:

`$ ./run.sh`

This `run.sh` script will call on three other scripts - `py.sh`, `begin.sh`, and `serve.sh`.
The `py.sh` script launches the Python script for data collection and processing.
The `begin.sh` script launches the Chromium browser, opening the correct link
(http://raspberrypi:8000/).
The `serve.sh` script opens the websocket connection, reading from the end of the
`log.txt` file (where the data is recorded) and sending those values to the client
(javascript code).

To terminate the websocket connection, use `^C` and then use the `killprocesses.sh`
script (command `$ ./killprocesses.sh`) to terminate the appropriate processes.
