# SVX SDS
## Handling Tetra SDS, status and LIP data for SVXLink and APRS

## Features:
* Initialization of PEI interface
* Using status messages as substitute for DTMF 0..9, * and #
* Decide who (which ISSI) is allowed to send SVXLink commands
* Connecting to EchoLink nodes using SDS (text) messages
* Decode LIP data
* Lookup ISSI in DMR MARC database
* Position, direction and speed storage in MySQL database
* Position, direction and speed upload to aprs.fi
* Control SVXLink squelch via pseudo TTY and PEI output

## Installation
1. Copy the files to a directory of your choice
1. Create a new MySQL database
1. sudo copy the file svxsds.cfg.default to /etc/ and rename it to svxsds.cfg
1. Open /etc/svxsds.cfg and adjust the settings:
	* Set the flags to use APRS, MySQL storage and ACL
	* MySQL access data (server address, port, username password, database name)
	* Your credentials for aprs.fi
	* The serial port interface characteristics (interface and speed)
1. Open the file 'svxsds.service' with an editor of your choice and adjust the last section of the line 'ExecStart=...' to point to the directory where you've copied the files to.
1. After saving 'svxsds.service' sudo copy the file to the directory /lib/systemd/system
1. Enable the service so it starts on boot (sudo systemctl enable svxsds)
1. Start the service (sudo systemctl start svxsds)

__*Important to make sure SVXLink runs BEFORE launching svxsds.service!*__

## Config file
__use_mysql__ (True / False): determines whether or not position data is to be stored in a MySQL table

__use_aprs__ (True / False): determines wheter or not data is to be send to aprs.fi

__use_acl__ (True / False): 'True' means the ISSI is checked against the MySQL table to determine whether or not the use is allowed to send commands. 'False' means everybody is allowed to send commands to SVXLink.

__db_user__: MySQL database user name

__db_pw__: MySQL database password

__db_host__: URI or IP address of the database server

__db_port__: Port number to connect to MySQL server (default 3306)

__db_database__: Database name for the TetrAPRS data

__db_table__: Table name for the TetrAPRS raw messages

__db_acl__: Access Control List to register users with APRS symbol etc

__aprsuser__: Username for aprs.fi

__aprspw__: Password for aprs.fi

__use_digsquelch__ (True/False): 'True' means the SVXLink squelch is controlled via pseudo TTY commands

__pty_digsquelch__: Path to the pseudo TTY for squelch as defined (and uncommented) in rx section in svxlink.conf

__port__: Path to the serial device (ttyAMA0 = serial port via RPi GPIO, ttyUSBx = USB level converter)

__speed__: Serial speed of the radio as set via CPS

## Work in progress
* APRS Status integration
* APRS change symbol via SDS
* Repeater response via SDS
