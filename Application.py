import GUI
import Settings
import Socket
import Initialize 
import Read
from UserList import UserList

class Application():
    __gui = ''
    __connected = False
    __logNames = False
    __socket = ''
    __userList = UserList()
    __saveFile = ''
    __addOnCommand = False
    __addingCommand = "!join"

    def __init__(self):
        self.__gui = GUI.GUI(self, GUI.Tk())
        Settings.loadCredentials(self.__gui)

    def processLine(self, line):
        if __addOnCommand and not isJoin(line, __addingCommand):
            return
        self.addToList(getUser(line), getMessage(line))
        
    def addToList(self, user, message):
        if not self.__logNames:
            return
        self.__userList.addToList(user, message, self.__gui.getChatBox(), self.__gui.getIngoreStr(), self.__gui.getSaveStr())
        if self.__userList.size() == 1 and Settings.getSaveFileFromKey() != self.__gui.getSaveStr():
            saveFileInKey(self.getSaveStr())
    
    def connectSocket(self):
        if not self.isConnectionHealthy():
            if (self.__gui.getOauthStr() and self.__gui.getNameStr() and self.__gui.getChnlStr()):
                self.__socket = Socket.openSocket(str(self.__gui.getOauthStr()), str(self.__gui.getNameStr()), str(self.__gui.getChnlStr()))
                self.isConnected(Initialize.joinRoom(self.__socket), True)

    def isConnected(self, boolean=None, fromConnection=False):
        if boolean != None and boolean != self.__connected:
            self.__gui.setConnecButton(boolean, fromConnection)
            self.__connected = boolean
        return self.__connected

    def sendMessage(self, message=None):
        if not self.__socket:
            return
        if not message:
            Socket.sendMessage(self.__socket)
        else:
            Socket.sendMessage(self.__socket, message, self.getChnlStr())

    def recvBuff(self):
        return Socket.recv_timeout(self.__socket)

    def isConnectionHealthy(self):
        return self.isConnected() and self.__gui.isConnectActive()

    def isLoggingActive(self, boolean=None):
        if boolean != None:
            self.__logNames = boolean
        self.__logNames = self.__logNames and self.isConnectionHealthy()
        return self.__logNames

    def deleteList(self):
        self.__userList.deleteList()

    def setConnection(self, boolean):
        if boolean:
            self.connectSocket()
        else:
            self.__socket.close()
            self.isConnected(False)

    def after(self, time, method):
        if self.__gui:
            self.__gui.after(time, method)

    def mainloop(self):
        if self.__gui:
            self.__gui.mainloop()

            