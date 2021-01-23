import MySQLdb
import configparser
import logging

# get configuration settings
config = configparser.ConfigParser()
config.read('/etc/svxsds.cfg')
db_user = config.get('mysql','db_user')
db_pw = config.get('mysql','db_pw')
db_host = config.get('mysql','db_host')
db_database = config.get('mysql','db_database')
db_table = config.get('mysql','db_acl')

logger = logging.getLogger(__name__)

def ACL_InitDB():
	# create connector
	mydb = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pw,db=db_database)

	# create cursor
	dbcursor = mydb.cursor()
	checkstring = 'SHOW TABLES LIKE "' + db_table + '"'
	result = dbcursor.execute(checkstring)
	if result == 1:
		mydbcursor.close()
		mydb.close()
		return()
	if result == 0:
		createstring = 'CREATE TABLE IF NOT EXISTS ' + db_table + '(acl_ID INT NOT NULL AUTO_INCREMENT,acl_ISSI INT NOT NULL,acl_call VARCHAR(10) NULL,acl_name VARCHAR(20) NULL,PRIMARY KEY (acl_ID))'
		dbcursor.execute(createstring)
		logger.info('Created new table')
		mydbcursor.close()
		mydb.close()
		return()


def IsInACL(tempISSI):
	mydb = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pw,db=db_database)
	dbcursor = mydb.cursor()
	querystring = 'SELECT * FROM `' + db_table + '` WHERE `acl_ISSI` = ' + tempISSI
	result = dbcursor.execute(querystring)
	if result == 1:
		return(True)
	if result == 0:
		return(False)

