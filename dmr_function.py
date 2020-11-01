# load libraries
import json
import urllib3
import logging

logger = logging.getLogger(__name__)

http = urllib3.PoolManager()

# variables
URI = "https://database.radioid.net/api/dmr/user/"

def GetCallSign(dmrID):
	global URI
	try:
		int(dmrID)
		URI = URI + '?id=' + dmrID
		response = http.request('GET',URI)
		response = json.loads(response.data.decode('utf-8'))
		logger.debug('GetCallSign - DMRID : ' + dmrID + ' - ' + response['results'][0]['callsign'])
		return(response['results'][0]['callsign'])
	except:
		logger.error('GetCallSign - Invalid input: ' + dmrID)
