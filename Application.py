import GUI
import Settings
import Socket_local
import Initialize 
import random
from Read import getUser, getMessage, isCommand
from UserList import UserList

joinCmd = "!join"
pickCmd = "!pick"

class Application():
    __gui = ''
    __connected = False
    __logNamesHello = False
    __logNamesJoin = False
    __socket = ''
    __userList = UserList()
    __saveFile = ''

    def __init__(self):
        self.__gui = GUI.GUI(self, GUI.Tk())
        Settings.loadCredentials(self.__gui)

    def processLine(self, line):
        if self.__logNamesHello:
            self.addToList(getUser(line), getMessage(line))
        elif self.__logNamesJoin:
            message = getMessage(line)
            if  message.startswith(joinCmd):
                message = message.replace(joinCmd, '', 1)
                self.addToList(getUser(line), message)
            elif message.startswith(pickCmd) and getUser(line).lower() == self.__gui.getChnlStr().lower():
                self.pickUser()
                return

    def pickUser(self):
        if self.__userList.size() == 0:
            self.sendMessage("No one has joined yet... :( ... ")
            return

        chosen=self.__userList.selectEntry(random.randint(0, self.__userList.size()-1), self.__gui.getChatBox()).split(":   ")
        user = chosen[0]
        message = chosen[1].strip()
        if len(chosen) == 2 and message:
            self.sendMessage("Winner! User: "+ user +" with message "+ message)
        else:
            self.sendMessage("Winner! User: "+ user)
       
    def addToList(self, user, message):
        if not self.__logNamesHello and not self.__logNamesJoin:
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
            self.__socket.sendMessage(message, self.__gui.getChnlStr())

    def recvBuff(self):
        if self.__socket != '':
            return self.__socket.recv_timeout()

    def isConnectionHealthy(self):
        return self.isConnected() and self.__gui.isConnectActive()

    def isLoggingActiveHello(self, boolean=None):
        if boolean != None:
            self.__logNamesHello = boolean
        self.__logNamesHello = ( self.__logNamesHello and self.isConnectionHealthy() )
        return self.__logNamesHello

    def isLoggingActiveJoin(self, boolean=None):
        if boolean != None:
            self.__logNamesJoin = boolean
        self.__logNamesJoin = ( self.__logNamesJoin and self.isConnectionHealthy() )
        return self.__logNamesJoin

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

            