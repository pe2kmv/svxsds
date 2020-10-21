# dependencies
import time
import serial
import subprocess
from statuslist import status_table as status

# settings
ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 1
ser.xonoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 2

if ser.isOpen:
	ser.close()

def ProcessSDS (rawsds):
	rawsds = rawsds.split("\\r\\n")
	print(rawsds[2])
	prep_echo = 'echo "' + status[rawsds[2]] + '" > /tmp/pty_ctl'
	print(prep_echo)
	subprocess.call(prep_echo, shell=True)
	return()

# open serial port
try:
	ser.open()
except:
	print("Error opening serial port")
	exit()

if ser.isOpen:

	try:
		ser.flushInput()
		ser.flushOutput()
		while True:
			response = ser.readall()
			if len(response) >0:
				response = str(response)
				ProcessSDS(response)

	except:
		ser.close()
		print("script error")
		exit(0)
