import logging

logger = logging.getLogger(__name__)

def ProcessLIP(tmpMessage):
	MessageType = tmpMessage[1:3]
	logging.debug('ProcessLIP - MessageType: '+ MessageType)
	if MessageType == 'A0':
		logging.debug('ProcessLIP - Start decoding short LIP')
		DecodeShortLIPLong(tmpMessage)
		DecodeShortLIPLat(tmpMessage)
	tmpMessage = tmpMessage[2:]
	logging.debug('ProcessLIP - Message: ' + tmpMessage)
	return()

def DecodeShortLIPLong(tmpMessage):
	logging.debug('DecodeShortLIP - Message: ' + tmpMessage)
	PosLong = int(tmpMessage[2],16) << 25
	PosLong = PosLong + (int(tmpMessage[3],16) << 21)
	PosLong = PosLong + (int(tmpMessage[4],16) << 17)
	PosLong = PosLong + (int(tmpMessage[5],16) << 13)
	PosLong = PosLong + (int(tmpMessage[6],16) << 9)
	PosLong = PosLong + (int(tmpMessage[7],16) << 5)
	PosLong = PosLong + ((int(tmpMessage[8],16) + 0x08) << 1)
	PosLong  = PosLong * 360 / 33554432
	logging.debug('DecodeShortLIPLong - Longitude: ' + str(PosLong))
	return(PosLong)

def DecodeShortLIPLat(tmpMessage):
	PosLat = (int(tmpMessage[9],16) + 0x0) << 22
	PosLat = PosLat + (int(tmpMessage[10],16) << 18)
	PosLat = PosLat + (int(tmpMessage[11],16) << 14)
	PosLat = PosLat + (int(tmpMessage[12],16) << 10)
	PosLat = PosLat + (int(tmpMessage[13],16) << 6)
	PosLat = PosLat + (int(tmpMessage[14],16) << 2)
	PosLat = PosLat + ((int(tmpMessage[15],16) + 0x0C) >> 2)
	PosLat = PosLat * 180 / 33554432
	logging.debug('DecodeShortLIPLat = Latitude: '+ str(PosLat))
	return(PosLat)
