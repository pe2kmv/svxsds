def ProcessLIP(liptext):
	try:
		tmpLong = GetLongitude(liptext)
		tmpLat = GetLatitude(liptext)
		return(str(tmpLat) + ',' + str(tmpLong))
	except:
		return()

def GetPDUType(liptext):
	pdu = extractKBits(liptext,0,2)
	return(pdu)

def GetPDUExtension(liptext):
	pduext = extractKBits(liptext,2,4)
	return(pduext)

def ExtractTimeType(liptext):
	timetype = extractKBits(liptext,6,2)
	return(timetype)

def GetTimeType(liptext):
	timetype = ExtractTimeType(liptext)
	return(DecodeTimeType(timetype))

def GetTimeData(liptext):
	timetype = ExtractTimeType(liptext)
	startbit = 8 # PDU type 2; PDU type extension 4; Time type 2
	if timetype == 1:
		timedata = extractKBits(liptext,8,2)
		return(DecodeTimeElapsed(timedata))
	if timetype == 2:
		day = extractKBits(liptext,startbit,5)
		hour = extractKBits(liptext,startbit + 5,5)
		min = extractKBits(liptext,startbit + 10,6)
		sec = extractKBits(liptext,startbit + 16,6)
		return(str(day) + ',' + str(hour) + ',' + str(min) + ',' + str(sec))

def ExtractPositionError(liptext):
	if GetPDUType(liptext) == 0:
		poserr = extractKBits(liptext,53,3)
		return(poserr)

def GetDirection(liptext):
	if GetPDUType(liptext) == 0:
		dir = extractKBits(liptext,63,4)
		dir = round(dir * 22.5) # direction in steps of 22.5 degrees
		return(dir)
	if GetPDUType(liptext) == 1:
		diroffset = GetDirectionOffset(ExtractVelocityType(liptext))
		return(diroffset)


# extract type of additional data
# 0 = reason for sending
# 1 = user defined data
def GetTOAD(liptext):
	if GetPDUType(liptext) == 1:
		startbit = 16 # PDU type 2; PDU type ext 4; Time type 2; Location shape 4; velocity type 3; acknowledgement req 1
		startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) # add var bitlength for time type
		startbit = startbit + BitLengthLocationShape(ExtractLocationShape(liptext)) # add var bitlength for location shape
		startbit = startbit + BitLengthVelocityType(ExtractVelocityType(liptext)) #add var bitlength for velocity type
		toad = extractKBits(liptext,startbit,1)
		return(toad)

def ExtractReasonForSending(liptext):
	if GetPDUType(liptext) == 0:
		startbit = 68
	if GetPDUType(liptext) == 1:
		startbit = 17 # PDU type 2; PDU type ext 4; Time type 2; Location shape 4; velocity type 3; acknowledgement req 1; Type of additional data 1
		startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) # add var bitlength for time type
		startbit = startbit + BitLengthLocationShape(ExtractLocationShape(liptext)) # add var bitlength for location shape
		startbit = startbit + BitLengthVelocityType(ExtractVelocityType(liptext)) #add var bitlength for velocity type
	rfs = extractKBits(liptext,startbit,8)
	return(rfs)


def GetRFS(liptext):
	rfs = ExtractReasonForSending(liptext)
	return(DecodeReasonForSending(rfs))

def GetT5StartBit(liptext):
	startbit = 25 # PDU type 2; PDU type ext 4; Time type 2; Location shape 4; velocity type 3; acknowledgement req 1; Type of additional data 1; reason for sending or user def data 8
	startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) # add var bitlength for time type
	startbit = startbit + BitLengthLocationShape(ExtractLocationShape(liptext)) # add var bitlength for location shape
	startbit = startbit + BitLengthVelocityType(ExtractVelocityType(liptext)) #add var bitlength for velocity type
	return(startbit)

def ExtractLocationShape(liptext):
	startbit = 8 #PDU type 2; PDU type extension 4; Time type 2
	startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) # add variable bitlength for specific time type
	locshape = extractKBits(liptext,startbit,4)
	return(locshape)

def GetLocationError(liptext):
	return(DecodePositionError(ExtractPositionError(liptext)))

def GetLocationShape(liptext):
	locshape = ExtractLocationShape(liptext)
	return(DecodeLocationShape(locshape))

def GetLongitude(liptext):
	if GetPDUType(liptext) == 0:
		startbit = 4
	if GetPDUType(liptext) == 1:
		startbit = 12 #PDU type 2; PDU type ext 4; Time type 2; Location shape 4
		startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) #add variable bitlength for time type
	lon = extractKBits(liptext,startbit,25)
	lon = (lon * 360/(2**25))
	return(lon)

def GetLatitude(liptext):
	if GetPDUType(liptext) == 0:
		startbit = 29
	if GetPDUType(liptext) == 1:
		startbit = 12
		startbit = 37 #offset + 25 bits used by longitude
		startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) #add variable bitlength for time type
	lat = extractKBits(liptext,startbit,24)
	lat = lat * 180/(2**24)
	if lat > 90:
		lat = lat - 180
	if lat < -90:
		lat = lat + 180
	return(lat)

def ExtractVelocityType(liptext):
	startbit = 12 # PDU type 2; PDU type ext 4; TimeType 2; Location shape 4
	startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) # add variable part for time type
	startbit = startbit + BitLengthLocationShape(ExtractLocationShape(liptext)) # add variable part for location shape
	veltype = extractKBits(liptext,startbit,3)
	return(veltype)

def GetVelocityType(liptext):
	veltype = ExtractVelocityType(liptext)
	return(DecodeVelocityType(veltype))

def GetHVelocity(liptext):
	if GetPDUType(liptext) == 0:
		startbit = 56
	if GetPDUType(liptext) == 1:
		startbit = 15 #PDU type 2; PDU Type ext 4; Time type 2; Location shape 4; Velocity type 3
		startbit = startbit + BitLengthTimeType(ExtractTimeType(liptext)) # add variable bits for time type
		startbit = startbit + BitLengthLocationShape(ExtractLocationShape(liptext)) # add variable bits for location shape
	hvel = extractKBits(liptext,startbit,7)
	return(DecodeHVelocity(hvel))

def GetAltitude(liptext):
	locshape = ExtractLocationShape(liptext)
	if locshape == 4:
		bitoffset = 49

	alt = extractKBits(liptext,15 + bitoffset + GetTimeType(liptext),11)
	return(DecodeAltitude(alt))

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


def DecodeTimeElapsed(timedata):
	switcher = {
	0:	"< 5s",
	1:	"< 5m",
	2:	"< 30m",
	3:	None
	}
	return(switcher.get(timedata))

def BitLengthTimeType(timetype):
	switcher = {
	0:	None,
	1:	2,
	2:	22,
	3:	None
	}
	return(switcher.get(timetype))

def DecodeTimeType(timetype):
	switcher = {
	0:	"None",
	1:	"Time elapsed",
	2:	"Time of position",
	3:	"Reserved"
	}
	return(switcher.get(timetype))

def BitLengthLocationShape(locshape):
	switcher = {
	0:	0,	# no shape
	1:	49,	# location point
	2:	55,	# location circle
	3:	72,	# location ellipse
	4:	61,	# location point with altitude
	5:	67,	# location circle with altitude
	6:	84,	# location ellipse with altitude
	7:	70,	# location circle with altitude and altitude uncertainty
	8:	87,	# location ellipse with altitude and altitude uncertainty
	9:	100,	# location arc
	10:	52,	# location point and position error
	11:	None,	# reserved
	12:	None,	# reserved
	13:	None,	# reserved
	14:	None,	# reserved
	15:	None,	# location shape extension
	}
	return(switcher.get(locshape))

def DecodeLocationShape(locshape):
	switcher = {
	0:	"No shape",
	1:	"Location point",
	2:	"Location circle",
	3:	"Location ellipse",
	4:	"Location point with altitude",
	5:	"Location circle with altitude",
	6:	"Location elipse with altitude",
	7:	"Location circle with altitude and altitude uncertainty",
	8:	"Location ellipse with altitude and altitude uncertainty",
	9:	"Location arc",
	10:	"Location point and position error",
	11:	"Reserved",
	12:	"Reserved",
	13:	"Reserved",
	14:	"Reserved",
	15:	"Reserved"
	}
	return(switcher.get(locshape))


def BitLengthVelocityType(veltype):
	switcher = {
	0:	0,	# No velocity information
	1:	7,	# Horizontal velocity
	2:	10,	# Horizontal velocity with uncertainty
	3:	15,	# Horizontal velocity and vertical velocity
	4:	21,	# Horizontal velocity and vertical velocity with uncertainty
	5:	15,	# Horizontal velocity with direction of travel extended
	6:	21,	# Horizontal velocity with direction of travel extended and uncertainty
	7:	32	# Horizontal velocity and vertical velocity with direction of travel extended and uncertainty
	}
	return(switcher.get(veltype))

def GetDirectionOffset(veltype):
	switcher = {
	0:	None,	# No direction information
	1:	None,	# No direction information
	2:	None,	# No direction information
	3:	None,	# No direction information
	4:	None,	# No direction information
	5:	8,	# Bit 8 from velocity type start
	6:	11,	# Bit 11 from velocity type start
	7:	22	# Bit 22 from velocity type start
	}
	return(switcher.get(veltype))

def DecodeVelocityType(veltype):
	switcher = {
	0:	"No velocity information",
	1:	"Horizontal velocity",
	2:	"Horizontal velocity with uncertainty",
	3:	"Horizontal velocity and vertical velocity",
	4:	"Horizontal velocity and vertical velocity with uncertainty",
	5:	"Horizontal velocity with direction of travel extended",
	6:	"Horizontal velocity with direction of travel extended and uncertainty",
	7:	"Horizontal velocity and vertical velocity with direction of travel extended and uncertainty"
	}
	return(switcher.get(veltype))

def DecodeHVelocity(hvel):
	if hvel <29:
		return(hvel)
	if hvel > 28 and hvel < 127:
		return(28 * (1.038 ** (hvel-28)))
	if hvel == 127:
		return(None)

def DecodeAltitude(alt):
	altoffset = -200
	if alt < 1202:
		alt = altoffset + alt
	if alt >= 1202 and alt < 1927:
		alt = (2*(alt-1201)) + 1000
	if alt >= 1927:
		alt = 75*(alt-1926) + 2450 
	return(alt)

def DecodePositionError(poserr):
	switcher = {
	0:	2,
	1:	20,
	2:	200,
	3:	2000,
	4:	20000,
	5:	200000,
	6:	200001,
	7:	None
	}
	return(switcher.get(poserr))

def DecodeReasonForSending(rfs):
	switcher = {
	0:	"Subscriber unit is powered ON",
	1:	"Subscriber unit is powered OFF",
	2:	"Emergency condition is detected",
	3:	"Push-to-talk condition is detected",
	4:	"Status",
	5:	"Transmit inhibit mode ON",
	6:	"Transmit inhibit mode OFF",
	7:	"System access (TMO ON)",
	8:	"DMO ON",
	9:	"Enter service (after being out of service)",
	10:	"Service loss",
	11:	"Cell reselection or change of serving cell",
	12:	"Low battery",
	13:	"Subscriber unit is connected to a car kit",
	14:	"Subscriber unit is disconnected from a car kit",
	15:	"Subscriber unit asks for transfer initialization configuration",
	16:	"Arrival at destination",
	17:	"Arrival at a defined location",
	18:	"Approaching a defined location",
	19:	"SDS type-1 entered",
	20:	"User application initiated",
	21:	"Lost ability to determine location",
	22:	"Regained ability to determine location",
	23:	"Leaving point",
	24:	"Ambience Listening call is detected",
	25:	"Start of temporary reporting",
	26:	"Return to normal reporting",
	32:	"Response to an immediate location request",
	129:	"Maximum reporting interval exceeded since the last location information report",
	130:	"Maximum reporting distance limit travelled since last location information report"
	}
	return(switcher.get(rfs))

def DecodeT5(t5):
	switcher = {
	0:	"Direction of travel and direction of travel accuracy",
	1:	"Extended user defined data",
	2:	"Horizontal position and horizontal position accuracy",
	3:	"Horizontal velocity and horizontal velocity accuracy",
	4:	"Location information destination",
	5:	"Location altitude and location altitude accuracy",
	6:	"Location message reference",
	7:	"Maximum information age",
	8:	"Maximum response time",
	9:	"Default enable/disable lifetime",
	10:	"Reserved",
	11:	"Request priority",
	12:	"Result code",
	13:	"SDS type-1 value",
	14:	"Start time",
	15:	"Status value",
	16:	"Stop time",
	17:	"Terminal or location identification",
	18:	"Reserved",
	19:	"Trigger definition",
	20:	"Trigger removal",
	21:	"Vertical velocity and vertical velocity accuracy",
	22:	"Temporary control parameter definition",
	23:	"Reserved",
	24:	"Reserved",
	25:	"Reserved",
	26:	"Reserved",
	27:	"Reserved",
	28:	"Reserved",
	29:	"Reserved",
	30:	"Reserved",
	31:	"Reserved"
	}
	return(switcher.get(t5))

def DecodeResultCode(rcode):
	switcher = {
	0:	"Success",
	1:	"System failure",
	2:	"Unspecified error",
	3:	"Unauthorized application",
	4:	"Unknown subscriber",
	5:	"Absent subscriber",
	6:	"Congestion in provider",
	7:	"Congestion in mobile network",
	8:	"Unsupported version",
	9:	"Insufficient resource",
	10:	"Syntax error",
	11:	"Protocol element not supported",
	12:	"Service not supported",
	13:	"Protocol element value not supported",
	14:	"Type of information not currently available",
	15:	"Required accuracy not achieved",
	16:	"Reserved",
	17:	"Reporting will stop",
	18:	"Time expired",
	19:	"Disallowed by local regulations",
	20:	"Reserved",
	21:	"No such request",
	22:	"User disabled location information report sending",
	23:	"Parameter values modified",
	24:	"Accepted",
	25:	"Accepted, but some of the triggers or accuracies are modified or are not supported",
	26:	"Triggers not supported",
	27:	"Report complete",
	81:	"Position method failure",
	200:	"Insufficient GPS satellites",
	201:	"Bad GPS geometry"
	}
	return(switcher.get(rcode))

