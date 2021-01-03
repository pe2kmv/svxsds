from statuslist import status_table as status
from newlip import ProcessLIP
from aprs_function import SendAPRS
from dmr_function import GetCallSign
import subprocess
import logging
from datetime import datetime
from mysql_function import add_to_db

logger = logging.getLogger(__name__)

def GetTypeSDS(rawsds):
	rawsds = str(rawsds)
	logger.debug('GetTypeSDS - Raw SDS: ' + rawsds)
	try:
		rawsds = rawsds.split('\\r\\n')
		rawsds[1][1:7] == 'CTSDSR'
		rawsds = rawsds[1]
		logger.debug('GetTypeSDS = Message type: '+ rawsds.split(',')[0][-2:])
		return(rawsds.split(',')[0][-2:])
	except:
		logger.debug('GetTypeSDS - Except detected, returning now')
		return('0')

def ValidatePosition(rawsds):
	rawsds = str(rawsds)
	try:
		TimeStamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		MessageBody = rawsds.split('\\r\\n')[2]
		logger.debug('ValidatePosition - Body: ' + MessageBody[0:2])
		tmpPosition = ProcessLIP(MessageBody[2:])
		logger.debug(rawsds)
		tmpLat = tmpPosition.split(',')[0]
		logger.debug('TempLat = ' + tmpLat)
		tmpLong = tmpPosition.split(',')[1]
		logger.debug('TempLong = '+ tmpLong)
		tmpIssi = GetIssi(rawsds)
		tmpCall = GetCallSign(rawsds)
		logger.debug('TempCall = ' + tmpCall) 
		if tmpCall != None and tmpLat != "0.0" and tmpLong != "0.0":
			logger.debug('Save to DB')
			add_to_db(TimeStamp,tmpIssi,tmpCall,rawsds.split('\\r\\n')[2])
			logger.debug('Switch to sendaprs')
			SendAPRS(tmpCall,tmpLat,tmpLong)
	except:
		return()

def ValidateSDS(rawsds):
	rawsds = str(rawsds)
	TimeStamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	logger.debug('ValidateSDS - Timestamp ' + TimeStamp)
	try:
		rawsds = rawsds.split('\\r\\n')
		MessageBody = bytearray.fromhex(rawsds[2])[4:].decode("utf-8")
		logger.debug('ValidateSDS - ' + MessageBody)
		if MessageBody[-1] != '#':
			MessageBody = MessageBody + '#'
		int(MessageBody[0:-1])
		return(True)
	except:
		logger.debug('ValidateSDS except found')
		return(False)

def ScreenSDS(rawsds):
	MessageType = GetTypeSDS(rawsds)
	logger.debug('ScreenSDS - Message type: ' + MessageType)
	if MessageType != '0':
		if MessageType == "12":
			# this is an SDS text message
			if ValidateSDS(rawsds) == True:
				ProcessSDS(rawsds)
		if MessageType == "13":
			# this is a status message
			ProcessStatus(rawsds)
		ValidatePosition(rawsds)
	else:
		logger.debug('ScreenSDS - Exiting')
		return()

def EchoSVXLink(echostring):
	try:
		subprocess.call(echostring, shell=True)
		logger.debug('EchoSVXLink - Sending echo: ' + echostring)
	except:
		logger.error('EchoSVXLink - Failed to send echo: ' + echostring)
		return()

def ProcessStatus(rawsds):
	rawsds = str(rawsds)
	rawsds = rawsds.split('\\r\\n')
	try:
		prep_echo = 'echo "' + status[rawsds[2]] + '" > /tmp/pty_ctl'
		logger.debug(prep_echo)
		EchoSVXLink(prep_echo)
	except:
		logger.error('Failed to process status: ' + str(rawsds))
		return()

def ProcessSDS(rawsds):
	rawsds = str(rawsds)
	rawsds = rawsds.split('\\r\\n')
	try:
		prep_echo = bytearray.fromhex(rawsds[2])[4:].decode("utf-8")
		if prep_echo[-1] != '#':
			prep_echo = prep_echo + '#'
		prep_echo = 'echo "' + prep_echo + '" > /tmp/pty_ctl'
		logger.debug('SDS Message echo: '+ prep_echo)
		EchoSVXLink(prep_echo)
	except:
		logger.error('Failed to process message: ' + str(rawsds))
		return()

def GetIssi(rawsds):
	try:
		issi = str(rawsds).split(',')[1]
		return(int(issi))
	except:
		return(None)
