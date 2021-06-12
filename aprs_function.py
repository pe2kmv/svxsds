# load necessary libraries
import aprslib
from logfunctions import *
import time
import configparser
from datetime import datetime
from aprslib.util import latitude_to_ddm, longitude_to_ddm, comment_altitude
from acl_function import GetAPRSSymbol,GetAPRSText
from mysql_function import MySQL_SetText,MySQL_SetSymbol
from aprssymbol import prim_table, alt_table

from sendmsg import SendSDS

# set variables
config = configparser.ConfigParser()
config.read('/etc/svxsds.cfg')
tetraprs_useaprs = config.get('overall','use_aprs')
aprs_user = config.get('aprs','aprsuser')
aprs_pw = config.get('aprs','aprspw')
aprs_host = config.get('aprs','aprshost')
aprs_port = config.get('aprs','aprsport')

# connect to APRS_IS
AIS = aprslib.IS(aprs_user,passwd=aprs_pw,host=aprs_host,port=aprs_port)

# get timestamp for APRS
timestamp = datetime.utcfromtimestamp(time.time()).strftime("%d%H%M") + 'z'

# this command changes APRS settings
def AprsCommand(tempissi,rawsds):
	try:
		tempcmd = rawsds.split(' ',1)[0]
		if tempcmd == 'settext':
			# this sets a new APRS beacon text in the database
			MySQL_SetText(tempissi,rawsds.split(' ',1)[1])
		if tempcmd == 'setsymb':
			# this sets a new APRS symbol
			tempsymb = rawsds.split(' ',1)[1]
			if tempsymb[0] == '/':
				# check whether or not this is a valid symbol
				if len(prim_table[tempsymb[1]]) > 0:
					# yes it's valid -> start MySQL query
					MySQL_SetSymbol(tempissi,tempsymb)
					SendSDS(tempissi,'APRS Symbol changed!')
			if tempsymb[0] == '\\':
				if len(alt_table[tempsymb[1]]) > 0:
					# also a valid symbol -> start MySQL query
					MySQL_SetSymbol(tempissi,tempsymb)
					SendSDS(tempissi,'APRS Symbol changed!')
		else:
			return()
	except:
		return()

def SendAPRS(tempCall, tempLat, tempLong,tempPayLoad):
	if tetraprs_useaprs != "True":
		return()
	# create floats
	tempLat = float(tempLat)
	tempLong = float(tempLong)
	tempSymbol = GetAPRSSymbol(tempCall,'CALL')
	tempPayLoad = tempPayLoad + GetAPRSText(tempCall,'CALL')
	if tempCall != None and tempLat != 0 and tempLong !=0:
		# get timestamp for APRS
		timestamp = datetime.utcfromtimestamp(time.time()).strftime("%d%H%M") + 'z'
		APRSString = tempCall + '>APRS,TCPIP*:@' + timestamp + latitude_to_ddm(tempLat) + tempSymbol[0] + longitude_to_ddm(tempLong) + tempSymbol[1] + tempPayLoad
		aprs_logger.info(APRSString)
		try:
			AIS.connect()
			AIS.sendall(APRSString)
			logger.debug('SendAPRS - APRS string sent - '+ APRSString)
			return()
		except:
			logger.error('SendAPRS - Failed to send APRS string')
			return()

def GetAPRSLat(tempLat):
	if float(tempLat) > 0:
		NS = 'N'
	if float(tempLat) < 0:
		NS = 'S'
	tempLat = str(tempLat)
	tempLat = tempLat.split('.')
	aprsLat = tempLat[0].zfill(2) + tempLat[1][0:2] + '.'+ tempLat[1][2:4] + NS
	return(aprsLat)

def GetAPRSLong(tempLong):
	if float(tempLong) > 0:
		EW = 'E'
	if float(tempLong) < 0:
		EW = 'W'
	tempLong = str(tempLong).split('.')
	aprsLong = tempLong[0].zfill(3) + tempLong[1][0:2] + '.' + tempLong[1][2:4] + EW
	return(aprsLong)
