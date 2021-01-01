import MySQLdb
import sys
import logging
import configparser

logger = logging.getLogger(__name__)

# get configuration
config = configparser.ConfigParser()
config.read('/home/pi/svx_sds/config.cfg')
tetraprs_user = config.get('mysql','db_user')
tetraprs_pw = config.get('mysql','db_pw')
tetraprs_host = config.get('mysql','db_host')
tetraprs_db = config.get('mysql','db_database')
tetraprs_table = config.get('mysql','db_table')

def add_to_db(TempTimeStamp,TempSDS):
	try:
		db = MySQLdb.connect(host=tetraprs_host,user=tetraprs_user,passwd=tetraprs_pw,db=tetraprs_db)
		print("db opened")
		cur = db.cursor()
		print("cursor created")
		print(TempTimeStamp)
		print(TempSDS)
		cur.execute("INSERT INTO tetraprs_raw (TimeStamp,SDS_RAW) VALUES ('" + TempTimeStamp + "','" + str(TempSDS) + "')")
		print("query executed")
		db.commit()
		print("database committed")
		cur.close()
		print("cursor closed")
	except:
		logger.error("AddToDB - Could not add to database")

