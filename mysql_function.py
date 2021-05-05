import MySQLdb
import sys
import configparser

from logfunctions import *
from newlip2 import *
from acl_function import IsInACL

# get configuration
config = configparser.ConfigParser()
#config.read('/home/pi/svx_sds/config.cfg')
config.read('/etc/svxsds.cfg')
tetraprs_usemysql = config.get('overall','use_mysql')
tetraprs_user = config.get('mysql','db_user')
tetraprs_pw = config.get('mysql','db_pw')
tetraprs_host = config.get('mysql','db_host')
tetraprs_db = config.get('mysql','db_database')
tetraprs_table = config.get('mysql','db_table')
tetraprs_acl = config.get('mysql','db_acl')

def SQLEsc(s):
	if s == None:
		return "NULL"
	else:
		return "'"+string.replace(s, "'", "''")+"'"

def add_to_db(TempTimeStamp,TempISSI, TempCallSign,TempSDS):
	print('Start add_to_db...')
	try:
		templat = GetLatitude(TempSDS[2:])
		templon = GetLongitude(TempSDS[2:])
		templocerror = GetLocationError(TempSDS[2:])
		temphvel = GetHVelocity(TempSDS[2:])
		tempdir = "'" + str(GetDirection(TempSDS[2:])) + "'"
		if tempdir == "'None'":
			tempdir = None
		db = MySQLdb.connect(host=tetraprs_host,user=tetraprs_user,passwd=tetraprs_pw,db=tetraprs_db)
		cur = db.cursor()
		cur.execute("INSERT INTO tetraprs_raw (TimeStamp,ISSI, CallSign,SDS_RAW,Latitude,Longitude,LocationError,HVelocity,Direction) VALUES ('" + TempTimeStamp +"','" + str(TempISSI) + "','" + TempCallSign   + "','" + str(TempSDS) + "','" + str(templat) + "','" + str(templon) + "','" + str(templocerror) + "','" + str(temphvel) + "'," + SQLEsc(tempdir) + ")")
		db.commit()
		cur.close()
	except:
		logger.error("AddToDB - Could not add to database")


def InitDB():
	# connector
	mydb = MySQLdb.connect(host=tetraprs_host,user=tetraprs_user,passwd=tetraprs_pw,db=tetraprs_db)

	# cursor
	dbcursor = mydb.cursor()
	checkstring = 'SHOW TABLES LIKE "' + tetraprs_table + '"'
	result = dbcursor.execute(checkstring)
	if result == 1:
		dbcursor.close()
		mydb.close()
		return()
	if result == 0:
		createstring = "CREATE TABLE IF NOT EXISTS " + tetraprs_table + " (TimeStamp datetime NOT NULL,SDS_RAW VARCHAR(254) NOT NULL, ISSI INT NOT NULL, CallSign VARCHAR(15),Longitude FLOAT, Latitude FLOAT, LocationError VARCHAR(50), HVelocity FLOAT,Direction FLOAT)"
		dbcursor.execute(createstring)
		logger.debug("Created MySQL table for LIP data")
		dbcursor.close()
		mydb.close()
		return()

# Set a new APRS beacon text in the database
def MySQL_SetText(tempissi,temptext):
	try:
		if (IsInACL(tempissi)) == True:
			db = MySQLdb.connect(host=tetraprs_host,user=tetraprs_user,passwd=tetraprs_pw,db=tetraprs_db)
			cur = db.cursor()
			cur.execute('UPDATE ' + tetraprs_acl + ' SET acl_aprs_text = "' + temptext + '" WHERE acl_ISSI = ' + tempissi)
			db.commit()
			cur.close()
			db.close()
			logger.debug('Updated APRS beacon text for ISSI ' + tempissi + ' to ' + temptext)
		else:
			logger.debug('ISSI not known in ACL')
		return()
	except:
		logger.debug('Could not update APRS beacon text')
		return()

def MySQL_SetSymbol(tempissi,tempsymbol):
	try:
		aprstable = tempsymbol[0]
		aprssymbol = tempsymbol[1]
		if (IsInACL(tempissi)) == True:
			db = MySQLdb.connect(host=tetraprs_host,user=tetraprs_user,passwd=tetraprs_pw,db=tetraprs_db)
			cur = db.cursor()
			cur.execute('UPDATE ' + tetraprs_acl + ' SET acl_aprs_table = "\\' + aprstable + '",acl_aprs_symbol = "' + aprssymbol + '" WHERE acl_ISSI = ' + tempissi)
			db.commit()
			cur.close()
			db.close()
			logger.debug('Updated APRS symbol for ISSI ' + tempissi + ' to ' + tempsymbol)
		else:
			logger.debug('ISSI not known in ACL')
		return()
	except:
		logger.debug('Could not update APRS beacon text')
		return()
