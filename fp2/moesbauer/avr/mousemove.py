import serial
ser = serial.Serial('/dev/ttyS0', 38400, timeout=0)
while(1):
	line = ser.readline()   # read a '\n' terminated line
	print line
	raw = line.split()
ser.close()

