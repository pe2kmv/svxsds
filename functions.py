from statuslist import status_table as status

def ScreenSDS(rawsds):
	rawsds = rawsds.split("\\r\\n")
	try:
		rawsds[1][1:7] == "CTSDSR"
		rawsds = rawsds[1]
		return(rawsds.split(",")[0][-2:])
	except:
		exit(0)

def ProcessStatus (rawsds):
	rawsds = rawsds.split("\\r\\n")
	try:
		prep_echo = 'echo "' + status[rawsds[2]] + '" > /tmp/pty_ctl'
#remove this line and next # for live version!
#       subprocess.call(prep_echo, shell=True)
	except:
		exit(0)

	return(prep_echo)

#def ScreenText(message):
	

def ProcessSDS(rawsds):
	rawsds = rawsds.split("\\r\\n")
	prepecho = rawsds[2]
	prep_echo = bytearray.fromhex(rawsds[2])[4:].decode("utf-8")
	prep_echo = 'echo "' + prep_echo + '" > /tmp/pty_ctl'
	return(prep_echo)
