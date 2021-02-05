from statuslist import status_table as status
from newlip import *
from aprs_function import SendAPRS
from dmr_function import GetCallSign
from acl_function import IsInACL
import subprocess
import logging
from datetime import datetime
from mysql_function import add_to_db
import configparser


# some handy generic functions
def ConvertToBool(tempstring):
	try:
		if tempstring.upper() == 'TRUE':
			return(True)
		if tempstring.upper() == 'FALSE':
			return(False)
	except:
		return()

stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

# get configuration settings
config = configparser.ConfigParser()
config.read('/etc/svxsds.cfg')
tetraprs_usemysql = config.get('overall','use_mysql').upper()
tetraprs_useaprs = config.get('overall','use_aprs').upper()
tetraprs_useacl = config.get('overall','use_acl').upper()
svx_usesquelch = ConvertToBool(config.get('svxlink','use_digsquelch').upper())
svx_ptysquelch = config.get('svxlink','pty_digsquelch')

logger = logging.getLogger(__name__)

def StripEmptyItems(temparray):
	return([x for x in temparray if x])


def ValidatePosition(rawsds):
	try:
		TimeStamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		MessageBody = rawsds[1]
		logger.debug('ValidatePosition - Body: ' + MessageBody[0:2])
		tmpPosition = ProcessLIP(MessageBody[2:])
		logger.debug(rawsds)
		tmpLat = tmpPosition.split(',')[0]
		logger.debug('TempLat = ' + tmpLat)
		tmpLong = tmpPosition.split(',')[1]
		logger.debug('TempLong = '+ tmpLong)
		logger.debug('Course: '+ str(GetDirection(MessageBody[2:])))
		logger.debug(GetHVelocity(MessageBody[2:]))
		if str(GetDirection(MessageBody[2:])) == "None" or str(GetHVelocity(MessageBody[2:])) == "None":
			tmpPayload = '   /   '
		else:
			tmpPayload = str(GetDirection(MessageBody[2:])).zfill(3)  + '/' + str(GetHVelocity(MessageBody[2:])).zfill(3)
		logger.debug('Direction = ' + str(tmpPayload))
		tmpIssi = GetIssi(rawsds[0])
		tmpCall = GetCallSign(rawsds[0])
		logger.debug('TempCall = ' + tmpCall) 
		add_to_db(TimeStamp,tmpIssi,tmpCall,rawsds[1])
		if tmpCall != 'No Call' and tmpLat != "0.0" and tmpLong != "0.0":
			if tetraprs_usemysql == "TRUE":
				logger.debug('Save to DB')
				add_to_db(TimeStamp,tmpIssi,tmpCall,rawsds[1])
			if tetraprs_useaprs == "TRUE":
				logger.debug('Switch to sendaprs')
				SendAPRS(tmpCall,tmpLat,tmpLong,tmpPayload)
	except:
		return()

def ValidateSDS(rawsds):
	TimeStamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	logger.debug('ValidateSDS - Timestamp ' + TimeStamp)
	try:
		MessageBody = bytearray.fromhex(rawsds[1][6:]).decode("utf-8")
		logger.debug('ValidateSDS - ' + MessageBody)
		if MessageBody[-1] != '#':
			MessageBody += '#'
		MessageBody[1:3].upper() == '#C'
		return(True)
	except:
		logger.debug('ValidateSDS except found')
		return(False)

def ScreenSDS(rawsds):
	sdsheader = StripEmptyItems(rawsds[0].split(','))
	if sdsheader[0][0:7] == '+CTSDSR':
		MessageType = sdsheader[0][-2:]
	else:
		return()
	logger.debug('ScreenSDS - Message type: ' + MessageType)
	if MessageType != '0':
		if MessageType == "12":
			# check whether this is a command, LIP or none
			if rawsds[1][0:2] == '0A':
				ValidatePosition(rawsds)
				return()

			if ValidateSDS(rawsds) == True:
				ProcessSDSCommand(rawsds)
				return()
		if MessageType == "13":
			# this is a status message
			ProcessStatus(rawsds)
			return()
	else:
		logger.debug('ScreenSDS - Exiting')
		return()

def PrepSerialData(serdata):
	serdata = serdata.decode('utf-8')
	serdata = serdata.replace('\r\n','|')
	serdata = StripEmptyItems(serdata.split('|'))
	return((serdata))

def FilterSerial(serdata):
	if serdata[0][0:6] == '+CTICN' and svx_usesquelch == True:
		# new call, incoming transmission detected - open squelch
		EchoSVXLink('echo "O" > ' + svx_ptysquelch)
		return('Incoming call notification')
	if serdata[0][0:5] == '+CTXG' and svx_usesquelch == True:
		# established call, incoming transmission detected - open squelch
		EchoSVXLink('echo "O" > ' + svx_ptysquelch)
		return('TX granted')
	if serdata[0][0:6] == '+CDTXC' and svx_usesquelch == True:
		# incoming transmission ended, close squelch
		EchoSVXLink('echo "Z" > ' + svx_ptysquelch)
		return('Transmision seized')
	if serdata[0][0:5] == '+CTCR' and svx_usesquelch == True:
		# end of reservation time, close squelch for sure
		EchoSVXLink('echo "Z" > ' + svx_ptysquelch)
		return('Call released')
	if serdata[0][0:6] == '+CTSDS':
		# incominig textmessage / status detected
		ScreenSDS(serdata)
		return('Text message received')
	else:
		return()

def EchoSVXLink(echostring):
	try:
		subprocess.call(echostring, shell=True)
		logger.debug('EchoSVXLink - Sending echo: ' + echostring)
	except:
		logger.error('EchoSVXLink - Failed to send echo: ' + echostring)
		return()

def ProcessStatus(rawsds):
	# check whether user is allowed to send commands
	if tetraprs_useacl == 'TRUE':
		tempISSI = str(GetIssi(rawsds))
		if IsInACL(tempISSI) == False:
			# user is NOT allowed - bail out
			logger.info('User not allowed to send command - ISSI = ' + tempISSI) 
			return()
	# either user is allowed or all users are allowed - continue routine
	try:
		prep_echo = 'echo "' + status[rawsds[1]] + '" > /tmp/pty_ctl'
		logger.debug(prep_echo)
		EchoSVXLink(prep_echo)
	except:
		logger.error('Failed to process status: ' + str(rawsds[1]))
		return()

def ProcessSDSCommand(rawsds):
	try:
		print(rawsds)
		tempsds = stripped(bytearray.fromhex(rawsds[1][6:]).decode("utf-8").strip())
		if tempsds[0:2].upper().strip() == '#C':
			# this is definitely a command
			prep_echo = tempsds[2:].strip()
			if prep_echo[-1] != '#':
				prep_echo += '#'
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
