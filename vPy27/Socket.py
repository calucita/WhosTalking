import socket
import time

HOST = "irc.twitch.tv"
PORT = 6667

def openSocket(PASS, IDENT, CHANNEL):
        s = socket.socket()
        s.connect((HOST, PORT))
        s.send("PASS " + PASS + "\r\n")
        s.send("NICK " + IDENT + "\r\n")
        s.send("JOIN #" +  CHANNEL + "\r\n")
        return s
	
def sendMessage(s, message="PONG :tmi.twitch.tv\r\n", CHANNEL=""):
        if not CHANNEL:
                s.send(message)
                return
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        s.send(messageTemp + "\r\n")

def recv_timeout(s, timeout=.250):
        data = ''
        #make socket non blocking
        s.setblocking(0)

        begin=time.time()
        while True:
                if data:
                    break
        
                #if you got no data at all bail out
                elif time.time()-begin > timeout:
                    break
        
                try:
                    data = s.recv(1024)
                except:
                    pass
                
        return data
