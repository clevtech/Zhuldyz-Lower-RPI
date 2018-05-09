import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
time.sleep(1) #give the connection a second to settle
arduino.write("Hello from Python!".encode('utf8'))
arduino.write("Hello from Python!".encode('utf8'))
while True:
    data = arduino.readline()
    if data:
        print(data.decode('utf8')) #strip out the new lines for now
		# (better to do .read() in the long run for this reason
