import MySQLdb
import sys
import logging
import configparser

from newlip import *

logger = logging.getLogger(__name__)

# get configuration
config = configparser.ConfigParser()
config.read('/home/pi/svx_sds/config.cfg')
tetraprs_usemysql = config.get('overall','use_mysql')
tetraprs_user = config.get('mysql','db_user')
tetraprs_pw = config.get('mysql','db_pw')
tetraprs_host = config.get('mysql','db_host')
tetraprs_db = config.get('mysql','db_database')
tetraprs_table = config.get('mysql','db_table')

def add_to_db(TempTimeStamp,TempSDS):
	if tetraprs_usemysql != "True":
		return()
	try:
		templat = GetLatitude(TempSDS[2:])
		templon = GetLongitude(TempSDS[2:])
		templocerror = GetLocationError(TempSDS[2:])
		temphvel = GetHVelocity(TempSDS[2:])
		db = MySQLdb.connect(host=tetraprs_host,user=tetraprs_user,passwd=tetraprs_pw,db=tetraprs_db)
		cur = db.cursor()
		logger.debug("MySQL - cursor created")
		logger.debug("INSERT INTO tetraprs_raw (TimeStamp,SDS_RAW,Latitude,Longitude,LocationError,HVelocity) VALUES ('" + TempTimeStamp + "','" + str(TempSDS) + "','"+ str(templat) + "','" + str(templon) + "','" + str(templocerror) + "','" + str(temphvel) + "')")
		cur.execute("INSERT INTO tetraprs_raw (TimeStamp,SDS_RAW,Latitude,Longitude,LocationError,HVelocity) VALUES ('" + TempTimeStamp + "','" + str(TempSDS) + "','"+ str(templat) + "','" + str(templon) + "','" + str(templocerror) + "','" + str(temphvel) + "')")
		db.commit()
		cur.close()
	except:
		logger.error("AddToDB - Could not add to database")

