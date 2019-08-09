import GUI
import Settings
import Socket
import Initialize 
from UserList import UserList
from DictLabel import *

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

    def addToList(self, user, message):
        if not self.__logNames:
            return
        self.__userList.addToList(user, message, self.__gui.ListChatters, self.__gui.IgnoreEntry.get(), self.__gui.SaveEntry.get())
        if self.__userList.size() == 1 and Settings.getSaveFileFromKey() != self.__gui.SaveEntry.get():
            saveFileInKey(self.SaveEntry.get())
    
    def connectSocket(self):
        if not self.isConnectionHealthy():
            if (self.__gui.OauthEntry.get() and self.__gui.NameEntry.get() and self.__gui.ChannelEntry.get()):
                self.__socket = Socket.openSocket(str(self.__gui.OauthEntry.get()), str(self.__gui.NameEntry.get()), str(self.__gui.ChannelEntry.get()))
                self.isConnected(Initialize.joinRoom(self.__socket), True)

    def isConnected(self, boolean=None, fromConnection=False):
        if boolean != None and boolean != self.__connected:
            if boolean:
                self.__gui.ConnectLabel[TXT]=txtConnd
                self.__gui.ConnectLabel[FG]=BL
                if fromConnection:
                    Settings.saveCredentials(self.__gui)
                    self.__gui.toggle_btn.config(relief=RSD, text=txtDisconnect)
            else:
                if fromConnection:
                    app.ChannelLabel.delete(0, END)
                    app.ChannelLabel.insert(txtERROR)
                else:
                    self.__gui.ConnectLabel[TXT]=txtNotConnd
                    self.__gui.ConnectLabel[FG]=RD
            self.__connected = boolean
        return self.__connected

    def sendMessage(self, message):
        if not self.__socket:
            return
        if not message:
            Socket.sendMessage(self.__socket)
        else:
            Socket.sendMessage(self.__socket, message, self.ChannelEntry.get())

    def recvBuff(self):
        return Socket.recv_timeout(self.__socket)

    def isConnectionHealthy(self):
        return self.isConnected() and self.__gui.toggle_btn.config(TXT)[-1] == txtDisconnect

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

            