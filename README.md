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
1. 
