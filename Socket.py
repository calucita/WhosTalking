import socket
import time

HOST = "irc.twitch.tv"
PORT = 6667

def openSocket(PASS, IDENT, CHANNEL):
        s = socket.socket()
        s.connect((HOST, PORT))
        __send(s, "PASS " + PASS + "\r\n")
        __send(s, "NICK " + IDENT + "\r\n")
        __send(s, "JOIN #" +  CHANNEL + "\r\n")
        return s
	
def sendMessage(s, message="PONG :tmi.twitch.tv\r\n", CHANNEL=""):
        if not CHANNEL:
                __send(s, message)
                return
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        __send(s, messageTemp + "\r\n")

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
                    data = s.recv(1024).decode()
                except:
                    pass
                
        return data

def __send(s, message):
        s.send(str.encode(message))