import GUI
import Settings
import Socket_local
import Initialize 
from Read import getUser, getMessage, isCommand
from UserList import UserList

class Application():
    __gui = ''
    __connected = False
    __logNames = False
    __socket = ''
    __userList = UserList()
    __saveFile = ''

    def __init__(self):
        self.__gui = GUI.GUI(self, GUI.Tk())
        Settings.loadCredentials(self.__gui)

    def processLine(self, line):
        self.addToList(getUser(line), getMessage(line))
        
    def addToList(self, user, message):
        if not self.__logNames:
            return
        self.__userList.addToList(user, message, self.__gui.getChatBox(), self.__gui.getIngoreStr(), self.__gui.getSaveStr())

        if self.__userList.size() == 1 and Settings.getSaveFileFromKey() != self.__gui.getSaveStr():
            Settings.saveFileInKey(self.__gui.getSaveStr())
    
    def connectSocket(self):
        if not self.isConnectionHealthy():
            if (self.__gui.getOauthStr() and self.__gui.getNameStr() and self.__gui.getChnlStr()):
                self.__socket = Socket_local.Socket_local()
                self.__socket.openSocket(str(self.__gui.getOauthStr()), str(self.__gui.getNameStr()), str(self.__gui.getChnlStr()))
                connectionError = Initialize.joinRoom(self.__socket, self.__gui.getNameStr())
                if connectionError:
                    self.__socket = ''
                self.isConnected(connectionError == 0, True, connectionError)

    def isConnected(self, boolean=None, fromConnection=False, errorCode=0):
        if boolean != None:
            self.__gui.setConnecButton(boolean, errorCode, fromConnection)
            self.__connected = boolean
            if (self.__connected):
                Settings.saveCredentials(self.__gui)
        return self.__connected

    def sendMessage(self, message=None):
        if self.__socket == '':
            # todo: maybe add error here?
            return
        if not message:
            self.__socket.sendMessage()
        else:
            self.__socket.sendMessage(message, self.getChnlStr())

    def recvBuff(self):
        if self.__socket != '':
            return self.__socket.recv_timeout()

    def isConnectionHealthy(self):
        return self.isConnected() and self.__gui.isConnectActive()

    def isLoggingActive(self, boolean=None):
        if boolean != None:
            self.__logNames = boolean
        self.__logNames = ( self.__logNames and self.isConnectionHealthy() )
        return self.__logNames

    def deleteList(self):
        self.__userList.deleteList()

    def setConnection(self, boolean):
        if boolean:
            self.connectSocket()
        else:
            if self.__socket != '':
                self.__socket.close()
                self.__socket = ''
            self.isConnected(False)

    def after(self, time, method):
        if self.__gui:
            self.__gui.after(time, method)

    def mainloop(self):
        if self.__gui:
            self.__gui.mainloop()

            