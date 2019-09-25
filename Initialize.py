import time
from Socket import sendMessage, recv_timeout

def joinRoom(s):
	readbuffer = ""
	start = time.time()
	while time.time() - start < 5:
		readbuffer = readbuffer + recv_timeout(s)
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for line in temp:
			if "failed" in line:
				return False
			if "Welcome" in line:                        
				#sendMessage(s, "I'm here! I'm calu's bot :3")
				return True
	return False

