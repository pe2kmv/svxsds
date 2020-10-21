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
	rawsds = rawsds.strip("\r\n")
	print(rawsds)
	prep_echo = 'echo "' + status[rawsds] + '" > /tmp/pty_ctl'
	subprocess.call(prep_echo, shell=True)
	return()

# open serial port
try:
	ser.open()
except:
	print("Error opening serial port")
	exit()

abc = 0
if ser.isOpen:

	try:
		ser.flushInput()
		ser.flushOutput()
		while True:
			response = ser.readline().decode('utf-8')
			if len(response) == 6:
				ProcessSDS(response)

	except:
		print("script error")
		exit(0)
