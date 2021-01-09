# load libraries
import sys
import serial
import time
import logging

from function_status import ScreenSDS
from mysql_function import InitDB

# settings
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrade = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 1
ser.xonoff = False
ser.rtscts = False
ser.dsrdtr = False

# setup logging
logging.basicConfig(filename='/var/log/svxsds.log',level=logging.DEBUG)
logger = logging.getLogger('__name__')

from initradio import InitRadio
#temp switch off InitRadio to speed up restart during testing phase
#InitRadio()


def OpenSerialPort():
	try:
		logging.debug('Opening serial port '+ ser.port)
		ser.open()
	except:
		logging.error('Error opening port ' + ser.port)
		exit()

def main_loop():
	while 1:
		response = ser.readall()
		if len(response) > 0:
			logging.debug(str(ScreenSDS(response)))

if __name__ == '__main__':
	print('Opening serial port')
	InitDB()
	OpenSerialPort()
	try:
		print('Running main loop')
		main_loop()
	except KeyboardInterrupt:
		print ('\nExiting by user request\n')
		sys.exit(0)
