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

__use_dapnet__ (True / False): 'True' means everybody is allowed to send DAPNET messages via SDS. 'False' disables the SDS to DAPNET gateway.

__db_user__: MySQL database user name

__db_pw__: MySQL database password

__db_host__: URI or IP address of the database server

__db_port__: Port number to connect to MySQL server (default 3306)

__db_database__: Database name for the TetrAPRS data

__db_table__: Table name for the TetrAPRS raw messages

__db_acl__: Access Control List to register users with APRS symbol etc

__aprsuser__: Username for aprs.fi

__aprspw__: Password for aprs.fi

__change_settings__ (True/False): 'True' allows to change APRS settings over the air

__use_digsquelch__ (True/False): 'True' means the SVXLink squelch is controlled via pseudo TTY commands

__pty_digsquelch__: Path to the pseudo TTY for squelch as defined (and uncommented) in rx section in svxlink.conf

__port__: Path to the serial device (ttyAMA0 = serial port via RPi GPIO, ttyUSBx = USB level converter)

__speed__: Serial speed of the radio as set via CPS

## Change APRS settings over the air
* Start the text message with #A followed by a space to flag an APRS settings command
* settext [new APRS beacon text]: this command changes the APRS beacon text to the string between the square brackets. Example: '#A settext Hello out there' changes the beacon text to 'Hello out there'
* setsymb [symbol table][symbol]: this command changes the APRS symbol at the map. Example: '#A setsymb /f' changes the symbol to a fire truck.

# Status
Status messages 0x9001 - 0x900C are reserved as shortcuts to send commands to SVXLink. The file 'statuslist.py' translates the hex message to the actual string which is to be send to SVXLink. Example: the radio is programmed with status 0x9001, programmed with text '1#' and assigned to one touch key [1]. Actually pressing the key [1] for longer than one second the radio sends status message 0x9001. The script looks up the message 0x9001 in the reference table in 'statuslist.py'.

Hex value | Message text | Hex value | Message text
--------- | ------------ | --------- | ------------
9001 | 1# | 9007 | 7#
9002 | 2# | 9008 | 8#
9003 | 3# | 9009 | 9#
9004 | 4# | 900A | 0#
9005 | 5# | 900B | *#
9006 | 6# | 900C | #

Status messages 0x8001 - 0x8006 have been reserved for the MIC-E position comments. Via the menu these status messages can be called and send to the node as a quick way to set the APRS position comment. 

Hex value | Message text
--------- | ------------
8001 | Off Duty
8002 | En Route
8003 | In Service
8004 | Returning
8005 | Committed
8006 | Special
8007 | Priority
8008 | EMERGENCY

## DAPNET via SDS
You can send DAPNET messages via SDS. Initiate a DAPNET message by starting the SDS text with '#D' (without quotes). After a space you'll have to enter the callsign of the receiver, again followed by a space. Finally you can enter the message text which can have a maximum of 80 characters.

## Work in progress
* APRS Status integration :white_check_mark:
* APRS change symbol via SDS :white_check_mark:
* Repeater response via SDS

## Major disclaimer
These scripts are only meant for hobby / ham radio purposes. Use is as always on own risk. In case something isn't working as expected: happy searching and puzzling!
