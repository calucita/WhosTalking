import time
import typing
import ObserverPattern
import Socket_local


class ConnectionManager:
    __socket: typing.Union[Socket_local.Socket_local, None]

    def __init__(self, observer: ObserverPattern.ObserverPattern) -> None:
        self.__socket = Socket_local.Socket_local()
        self.__connected = False
        self.__observer = observer

    def connectSocket(self, _name: str = "", _channel: str = "", _oauth: str = "") -> None:
        connectionError = 2
        for i in range(3):
            connectionError = self.__retriableConnect(_name, _channel, _oauth)
            if not connectionError:
                self.isConnected(connectionError == 0, True, connectionError)
                return
        self.isConnected(connectionError == 0, True, connectionError)

    def __retriableConnect(self, _name: str = "", _channel: str = "", _oauth: str = "") -> int:
        if self.__connected:
            return 0
        if self.__socket is None:
            self.__socket = Socket_local.Socket_local()
        if _oauth and _name and _channel:
            self.__socket.openSocket(str(_oauth), str(_name), str(_channel))
            connectionError = self.joinRoom(_name)
            if connectionError:
                self.__socket = None
            return connectionError
        return 2

    def isConnected(self, status: typing.Union[bool, None] = None, fromConnection=False, errorCode=0) -> bool:
        if status is not None:
            self.__observer.update(status, fromConnection, errorCode)
            self.__connected = status
        return self.__connected

    def setConnection(self, _connect: bool, _name: str = "", _channel: str = "", _oauth: str = "") -> None:
        if _connect:
            self.connectSocket(_name, _channel, _oauth)
        else:
            if self.__socket:
                self.__socket.close()
                self.__socket = None
            self.isConnected(False)

    def recvBuff(self):
        if self.__socket:
            return self.__socket.recv_timeout()

    def sendMessage(self, message=None, channel: str = ""):
        if self.__socket is None:
            # todo: maybe add error here?
            return
        if not message:
            self.__socket.sendMessage()
        else:
            self.__socket.sendMessage(message, channel)

    def joinRoom(self, expectedUser) -> int:
        readbuffer = ""
        start = time.time()
        while time.time() - start < 5 and self.__socket is not None:
            readbuffer = readbuffer + self.__socket.recv_timeout()
            temp = str.split(readbuffer, "\n")
            readbuffer = temp.pop()
            for line in temp:
                if "Login authentication failed" in line:
                    return 4

                if "Improperly formatted auth" in line:
                    return 3

                if expectedUser.lower() not in line.lower() and self.__socket:
                    self.__socket.close()
                    return 1

                if "failed" in line:
                    return 99

                if ":End of /NAMES list" in line:
                    # s.sendMessage("I'm here! I'm calu's bot :3")
                    return 0
        return 2
