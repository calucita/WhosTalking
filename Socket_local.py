import socket
import time

HOST = "irc.twitch.tv"
PORT = 6667

class Socket_local():
    __socket = ''
    
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def openSocket(self, PASS, IDENT, CHANNEL):
        if self.__socket == '':
            self.__socket = socket.socket()
            self.__socket.connect((HOST, PORT))
            self.__send("PASS " + PASS + "\r\n")
            self.__send("NICK " + IDENT + "\r\n")
            self.__send("JOIN #" +  CHANNEL + "\r\n")
        #return __socket

    def sendMessage(self, message="PONG :tmi.twitch.tv\r\n", CHANNEL=""):
        if not CHANNEL:
            self.__send(message)
            return
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        self.__send(messageTemp + "\r\n")

    def recv_timeout(self, timeout=.250):
        data = ''
        #make socket non blocking
        self.__socket.setblocking(0)

        begin=time.time()
        while True:
            if data:
                break
        
            #if you got no data at all bail out
            elif time.time()-begin > float(timeout):
                break
        
            try:
                data = self.__socket.recv(1024).decode()
            except:
                pass
                
        return data

    def __send(self, message):
        self.__socket.send(str.encode(message))

    def close(self):
        self.__socket.close()