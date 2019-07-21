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
	
def sendMessage(s, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        s.send(messageTemp + "\r\n")
        print("Sent: " + messageTemp)

def recv_timeout(the_socket,timeout=.250):
        data = ''
        #make socket non blocking
        the_socket.setblocking(0)

        begin=time.time()
        while True:
                if data:
                    break
        
                #if you got no data at all bail out
                elif time.time()-begin > timeout:
                    break
        
                try:
                    data = the_socket.recv(1024)
                except:
                    pass
                
        return data
