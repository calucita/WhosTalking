import typing
import GUI
import Settings
import ConnectionManager
import ObserverPattern
import ActivityController
import GUICallerInterface
from tkinter import Tk
from Tools import Modes
from Read import getUser, getMessage

joinCmd = "!join"
leavCmd = "!leave"
pickCmd = "!pick"


class Application(ObserverPattern.ObserverPattern, GUICallerInterface.GUICallerInterface):
    __activityController: typing.Union[ActivityController.ActivityController, None]

    def __init__(self):
        self.__gui = GUI.GUI(self, Tk())
        Settings.loadCredentials(self.__gui)
        self.__ConnectionManager = ConnectionManager.ConnectionManager(self)
        self.__activityController = ActivityController.ActivityController(self.__gui)

    def processLine(self, line):
        if "PING :tmi.twitch.tv" in line:
            self.sendMessage()
            return

        if self.__activityController and self.__activityController.isActivityEnabled():
            self.callActivities(getUser(line), getMessage(line))

    def pickUser(self):
        self.callActivities(str(self.__gui.getChnlStr()), "!pick")

    def callActivities(self, user, message):
        if not self.__activityController:
            return
        reply = self.__activityController.doAction(user, message)

        if reply:
            self.sendMessage(reply)

    def sendMessage(self, message=None):
        if not message:
            self.__ConnectionManager.sendMessage()
        else:
            self.__ConnectionManager.sendMessage(message, self.__gui.getChnlStr())

    def recvBuff(self):
        return self.__ConnectionManager.recvBuff()

    def isConnectionHealthy(self):
        return self.__ConnectionManager.isConnected() and self.__gui.isConnectActive()

    def loggingActive(self, mode: Modes, boolean: typing.Union[bool, None] = None) -> bool:
        if not self.__activityController:
            return False
        if boolean is not None:
            # Only disable the activity if the selected one is enabled
            if (
                not boolean
                and (not self.isConnectionHealthy() or self.__activityController.isActivityEnabled(mode))
                or (mode == Modes.NONE and boolean)
            ):
                self.__activityController.selectActivity(Modes.NONE)
                return False
            else:
                reply = self.__activityController.selectActivity(mode)
                if reply:
                    self.sendMessage(reply)
                if boolean:
                    if Settings.getSaveFileFromKey() != self.__gui.getSaveStr():
                        Settings.saveFileInKey(self.__gui.getSaveStr())

        return self.__activityController.isActivityEnabled(mode)

    def deleteList(self):
        if self.__activityController:
            self.__activityController.deleteList()

    def setConnection(self, _connect: bool) -> None:
        self.__ConnectionManager.setConnection(
            _connect, str(self.__gui.getNameStr()), str(self.__gui.getChnlStr()), str(self.__gui.getOauthStr())
        )

    def update(self, status: bool, fromConnection=False, errorCode=0) -> None:
        self.__gui.setConnectButton(status, errorCode, fromConnection)
        if status:
            Settings.saveCredentials(self.__gui)

    def after(self, time, method):
        if self.__gui:
            self.__gui.after(time, method)

    def chatCheck(self):
        if self.isConnectionHealthy():
            readbuffer = self.recvBuff()
            if readbuffer:
                temp = str.split(readbuffer, "\n")
                readbuffer = temp.pop()
                for line in temp:
                    # print(line)
                    self.processLine(line)

    def mainloop(self):
        if self.__gui:
            self.__gui.mainloop()
