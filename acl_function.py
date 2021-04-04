import MySQLdb
import configparser
from logfunctions import *

# get configuration settings
config = configparser.ConfigParser()
config.read('/etc/svxsds.cfg')
db_user = config.get('mysql','db_user')
db_pw = config.get('mysql','db_pw')
db_host = config.get('mysql','db_host')
db_database = config.get('mysql','db_database')
db_table = config.get('mysql','db_acl')

def ACL_InitDB():
	# create connector
	mydb = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pw,db=db_database)

	# create cursor
	dbcursor = mydb.cursor()
	checkstring = 'SHOW TABLES LIKE "' + db_table + '"'
	result = dbcursor.execute(checkstring)
	if result == 1:
		dbcursor.close()
		mydb.close()
		return()
	if result == 0:
		createstring = 'CREATE TABLE IF NOT EXISTS ' + db_table + '(acl_ID INT NOT NULL AUTO_INCREMENT,acl_ISSI INT NOT NULL,acl_call VARCHAR(10) NULL,acl_passwd VARCHAR(254),acl_name VARCHAR(20) NULL,acl_aprs_table VARCHAR(1),acl_aprs_symbol VARCHAR(1),acl_aprs_text VARCHAR(36),acl_auth_user BOOLEAN NOT NULL DEFAULT FALSE,PRIMARY KEY (acl_ID))'
		dbcursor.execute(createstring)
		logger.info('Created new table')
		dbcursor.close()
		mydb.close()
		return()


def IsInACL(tempISSI):
	mydb = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pw,db=db_database)
	dbcursor = mydb.cursor()
	querystring = 'SELECT acl_auth_user FROM `' + db_table + '` WHERE `acl_ISSI` = ' + tempISSI
	result = dbcursor.execute(querystring)
	if result == 1:
		if dbcursor.fetchone()[0] == 1:
			return(True)
		else:
			return(False)
	if result == 0:
		return(False)

def GetAPRSSymbol(tempINPUT,inputtype):
	mydb = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pw,db=db_database)
	dbcursor = mydb.cursor()
	if inputtype.upper() == "ISSI":
		querystring = 'SELECT CONCAT (acl_aprs_table, acl_aprs_symbol) AS fullsymbol FROM `' + db_table + '` WHERE `acl_ISSI` = ' + tempINPUT
	if inputtype.upper() == "CALL":
		querystring = 'SELECT CONCAT (acl_aprs_table, acl_aprs_symbol) AS fullsymbol FROM `' + db_table + '` WHERE `acl_call` = "' + tempINPUT + '"'

	try:
		result = dbcursor.execute(querystring)
		return(dbcursor.fetchone()[0])
	except:
		return('TA')

def GetAPRSText(tempINPUT,inputtype):
	mydb = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pw,db=db_database)
	dbcursor = mydb.cursor()
	if inputtype.upper() == "ISSI":
		querystring = 'SELECT acl_aprs_text FROM `' + db_table + '` WHERE acl_ISSI = ' + tempINPUT
	if inputtype.upper() == "CALL":
		querystring = 'SELECT acl_aprs_text FROM `' + db_table + '` WHERE acl_call = "' + tempINPUT + '"'
	try:
		result = dbcursor.execute(querystring)
		temptext = dbcursor.fetchone()[0]
		if temptext == '':
			return('TetrAPRS station')
		else:
			return(temptext)
	except:
		return('TetrAPRS station')
