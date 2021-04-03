import logging
import configparser
import requests
import json
logger = logging.getLogger(__name__)

# set variables
config = configparser.ConfigParser()
config.read('/etc/svxsds.cfg')
dapnet_user = config.get('dapnet','dapnetuser')
dapnet_pw = config.get('dapnet','dapnetpw')
dapnet_uri = config.get('dapnet','dapneturi')

def SendDapnet(tempsds):
	tempsds = tempsds.strip()
	tempsds = tempsds.split(' ',1)
	send_page(tempsds[0],3,'all','false',tempsds[1])

def send_page(msg_ric,func,trx,emr,msgtxt):
	req = requests.post(dapnet_uri,auth=(dapnet_user,dapnet_pw),json={'text':msgtxt,'callSignNames':[msg_ric],'transmitterGroupNames':[trx],'emergency':emr})
	logging.debug(req)

