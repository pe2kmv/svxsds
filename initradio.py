import serial
import time
import logging
import configparser

logger = logging.getLogger(__name__)

serialwait = 15 # Serial command timeout in seconds
atcommands = ['AT&F','AT+CTOM=6','AT+CTSP=1,3,131','AT+CTSP=1,3,130','AT+CTSP=2,0,0','AT+CTSP=1,2,20','AT+CTSP=1,2,24','AT+CTSP=1,2,25','AT+CTSP=1,1,11','AT+CTSP=1,3,137']

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
ser.timeout = 5
ser.writetimeout = 5
ser.xonoff = False
ser.rtscts = False
ser.dsrdtr = False

def OpenSerialPort():
	try:
		logger.debug('initradio - OpenSerialPort: Opening serial port '+ ser.port)
		ser.open()
	except:
		logger.error('initradio - OpenSerialPort: Error opening port ' + ser.port)
		exit()

def GetResponse(response):
	result = list(filter(None,response.decode('utf-8').split('\r\n')))
	if 'OK' in result:
		return(True)
	else:
		return(False)

def InitRadio():
	OpenSerialPort()

	for atc in atcommands:
		cmd = atc
		atc = atc + '\r'
		atc = atc.encode('utf-8')
		ser.write(atc)
		while 1:
			timeout = time.time() + serialwait
			response = ser.readall()
			if len(response) > 0 or time.time() > timeout:
				logger.debug('initradio - InitRadio: ' + cmd + ' : ' + (str(GetResponse(response))))
				break
	ser.close()
	return()
