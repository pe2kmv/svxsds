import MySQLdb
import configparser
import logging

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

# connector
mydb = MySQLdb.connect(
  host=tetraprs_host,
  user=tetraprs_user,
  passwd=tetraprs_pw,
  db=tetraprs_db
)

def InitDB():
	# cursor
	dbcursor = mydb.cursor()
	createstring = 'SHOW TABLES LIKE "' + tetraprs_table + '"'
	result = dbcursor.execute(createstring)
	if result == 1:
		dbcursor.close()
		mydb.close()
		return()
	if result == 0:
		createstring = "CREATE TABLE IF NOT EXISTS " + tetraprs_table + " (TimeStamp datetime NOT NULL,ISSI INT NOT NULL, CallSign VARCHAR(15),SDS_RAW VARCHAR(254) NOT NULL, Longitude FLOAT, Latitude FLOAT, LocationError VARCHAR(50), HVelocity FLOAT)"
		dbcursor.execute(createstring)
		logger.debug("Created MySQL table for LIP data")
		dbcursor.close()
		mydb.close()
		return()
