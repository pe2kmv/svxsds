# load libraries
import json
import urllib3
import logging

logger = logging.getLogger(__name__)

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
		logger.debug('GetCallSign - DMRID : ' + dmrID + ' - ' + response['results'][0]['callsign'])
		return(response['results'][0]['callsign'])
	except:
		logger.error('GetCallSign - Invalid input: ' + dmrID)

def GetDMRID(tmpSDS):
	tmpSDS = str(tmpSDS)
	try:
		tmpSDS = tmpSDS.split('\\r\\n')[1]
		tmpSDS = tmpSDS.split(',')[1]
		logger.debug('GetDMRID - DMRID = ' + tmpSDS)
		return(tmpSDS)
	except:
		logger.error('GetDMRID - Could not decode DMRID ('+ str(tmpSDS) + ')') 
		return('No Call')
