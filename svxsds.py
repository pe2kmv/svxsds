# dependencies
import sys
import time
import serial
import subprocess
from functions import ProcessStatus, ScreenSDS, ProcessSDS
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

pidi = "/tmp/svxsds.pid"

if ser.isOpen:
	ser.close()

# open serial port
def OpenSerialPort():
	try:
		ser.open()
	except:
		print("Error opening serial port")
		exit()

def main():
	if ser.isOpen:

		try:
			ser.flushInput()
			ser.flushOutput()
			while True:
				response = ser.readall()
				ser.flushInput()
				ser.flushOutput()
				if len(response) >0:
					response = str(response)
					MessageType = ScreenSDS(response)
					if MessageType == "13":
						svxmessage = ProcessStatus(response)
						print(MessageType + " - " + svxmessage)
						subprocess.call(svxmessage, shell=True)
					if MessageType == "12":
						svxmessage = ProcessSDS(response)
						print(MessageType + " - " + svxmessage)
						subprocess.call(svxmessage, shell=True)

		except:
			ser.close()
			print("script error")
			exit(0)


if __name__ == '__main__':
	try:
		OpenSerialPort()
		main()
	except KeyboardInterrupt:
		print >> sys.stderr, '\nExiting by user request\n'
		sys.exit(0)
