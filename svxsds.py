# load libraries
import sys
import serial
import time
#import logging
import configparser

from function_status import ScreenSDS,FilterSerial,PrepSerialData
from mysql_function import InitDB
from acl_function import ACL_InitDB
from logfunctions import *

# get configuration
config = configparser.ConfigParser()
config.read('/etc/svxsds.cfg')
ser_port = config.get('serial','port')
ser_speed = int(config.get('serial','speed'))

# settings
ser = serial.Serial()
ser.port = ser_port
ser.baudrade = ser_speed
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0.1
ser.xonoff = False
ser.rtscts = False
ser.dsrdtr = False

from initradio import InitRadio
#temp switch off InitRadio to speed up restart during testing phase
InitRadio()


def OpenSerialPort():
	try:
		logger.debug('Opening serial port '+ ser.port)
		ser.open()
	except:
		logger.error('Error opening port ' + ser.port)
		exit()

def main_loop():
	while 1:
		response = ser.readall()
		if len(response) > 0:
			response = PrepSerialData(response)
			logger.debug(str(FilterSerial(response)))

if __name__ == '__main__':
	print('Opening serial port')
	InitDB()
	ACL_InitDB()
	OpenSerialPort()
	try:
		print('Running main loop')
		main_loop()
	except KeyboardInterrupt:
		print ('\nExiting by user request\n')
		sys.exit(0)
