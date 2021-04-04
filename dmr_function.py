# load libraries
import json
import urllib3
from logfunctions import *

http = urllib3.PoolManager()

# variables
BASE_URI = "https://database.radioid.net/api/dmr/user/"

def GetCallSign(dmrID):
	global BASE_URI
	dmrID = GetDMRID(dmrID)
	logger.debug('GetCallSign - DMRID = ' + dmrID)
	try:
		int(dmrID)
		URI = BASE_URI + '?id=' + dmrID
		response = http.request('GET',URI)
		response = json.loads(response.data.decode('utf-8'))
		return(response['results'][0]['callsign'])
	except:
		logger.error('GetCallSign - Invalid input: ' + dmrID)
		return('No Call')

def GetDMRID(tmpSDS):
	try:
		tmpSDS = tmpSDS.split(',')[1]
		return(tmpSDS)
	except:
		logger.error('GetDMRID - Could not decode DMRID ('+ str(tmpSDS) + ')') 
		return('No Call')
