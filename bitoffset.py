def GetStartBit(liptext,attribute):
	startbit = 0
	pdutype = extractKBits(liptext,0,2)
	if pdutype == 0:
		# all start bits refer to short message
		switcher = {
		"TimeElapsed":	startbit + 2,
		"Longitude":	startbit + 4,
		"Latitude":	startbit + 29,
		"PositionError":	startbit + 53,
		"HorVelocity":	startbit + 56,
		"DirOfTravel":	startbit + 63,
		"TOAD":	startbit + 67,
		"ReasonSending":	startbit + 68
		}
		return(switcher.get(attribute))
	if pdutype == 1:
		startbit = startbit + 2 # move 2 bits to startbit of PDU Extension type
		if attribute == "PDUTypeExtension":
			return(startbit,4)
		startbit = startbit + 4 # move 4 bits to startbit of Time Data. Time Data first 2 bits determine which time data follows
		timetype = extractKBits(liptext,startbit,2) # determine type of Time Data
		timetypebitlength = TimeTypeBitLength(timetype)
		if attribute == "TimeData":
			return(startbit,timetypebitlength)
		startbit = startbit + 2 + timetypebitlength # move startbit for location data to previous startbit + 2 + variable time data bitlength
		locationshape = extractKBits(liptext,startbit,4) # first 4 bits determine the location shape (which has variable bit length)
		locationshapebitlength = LocationShapeBitLength(locationshape)
		if attribute == "LocationData":
			return(startbit,locationshapebitlength)
		startbit = startbit + 4 + locationshapebitlength # move the amount of bits belonging to the Location Shape. This determines the start bit of the Velocity Data
		velocitydata = extractKBits(liptext,startbit,3)
		velocitydatabitlength = VelocityDataBitLength(velocitydata)
		if attribute == "VelocityData":
			return(startbit,velocitydatabitlength)
		startbit = startbit + 3 + velocitydatabitlength # move variable bitlength for Velocity Data + 3 bits determining Velocity Type
		acrequest = extractKBits(liptext,startbit,1)
		acrequestbitlength = 1
		if attribute == "AckRequest":
			return(startbit,acrequestbitlength)
		startbit = startbit + 1 # acknowledgement request is just 1 bit
		toad = extractKBits(liptext,startbit,1)
		toadbitlength = TOADBitLength(toad)
		if attribute == "TOAD":
			return(startbit,toadbitlength)
		startbit = startbit + 1 + toadbitlength # move 1 + bitlength of additional data

def GetIdentifierBitLength(id):
	switcher = {
	"PDUType":	2,
	"PDUTypeExtension":	4,
	"TimeData":	2,
	"LocationData":	4,
	"VelocityData":	3,
	"AckRequest":	1,
	"TOAD":	1
	}
	return(switcher.get(id))

def TOADBitLength(toad):
	switcher = {
	0:	8, # Reason for sending = 8 bits
	1:	8 # User defined data = 8 bits
	}
	return(switcher.get(toad))

def TimeTypeBitLength(timetype):
	switcher = {
	0:	None,
	1:	2,
	2:	22,
	3:	None
	}
	return(switcher.get(timetype))

def LocationShapeBitLength(locshape):
	switcher = {
	0:	0,
	1:	49,
	2:	55,
	3:	72,
	4:	61,
	5:	67,
	6:	84,
	7:	70,
	8:	87,
	9:	100,
	10:	52,
	11:	4,
	12:	None,
	13:	None,
	14:	None,
	15:	None
	}
	return(switcher.get(locshape))

def VelocityDataBitLength(veltype):
	switcher = {
	0:	0,
	1:	7,
	2:	10,
	3:	15,
	4:	21,
	5:	15,
	6:	21,
	7:	32
	}
	return(switcher.get(veltype))

def extractKBits(hexstring,startbit,bitcount):
        liptext = int("0x" + hexstring,16)
        # convert number into binary first
        binary = bin(liptext)
        # remove first two characters
        binary = binary[2:]
        correction = (len(hexstring)*4) - len(binary)
        binary = ("0" * correction) + binary
        start = startbit
        end = startbit + bitcount
        # extract k  bit sub-string
        kBitSubStr = binary[start : end]
        # convert extracted sub-string into decimal again
        return(int(kBitSubStr,2))
