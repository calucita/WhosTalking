import typing
import GUI
import Settings
import ConnectionManager
import ObserverPattern
import ActivityController
import GUICallerInterface
from Tools import Modes
from Read import getUser, getMessage


class Application(ObserverPattern.ObserverPattern, GUICallerInterface.GUICallerInterface):
    __activityController: typing.Union[ActivityController.ActivityController, None]

    def __init__(self):
        self.__gui = GUI.GUI(self)
        # Settings.loadCredentials(self.__gui)
        self.__ConnectionManager = ConnectionManager.ConnectionManager(self)
        self.__activityController = ActivityController.ActivityController(self.__gui)

    def processLine(self, line) -> bool:
        if "PING :tmi.twitch.tv" in line:
            self.sendMessage()
            return False

        if self.__activityController and self.__activityController.isActivityEnabled():
            reply = self.callActivities(getUser(line), getMessage(line))

            if Settings.getSaveFileFromKey() != self.__gui.getSaveStr():
                Settings.saveFileInKey(self.__gui.getSaveStr())

            return reply
        return False

    def pickUser(self):
        self.callActivities(str(self.__gui.getChnlStr()), "!pick")

    def callActivities(self, user, message) -> bool:
        if not self.__activityController:
            return False
        reply = self.__activityController.doAction(user, message)

        if isinstance(reply, str):
            self.sendMessage(reply)
            return True
        if reply == True:
            return True
        return False

    def sendMessage(self, message=None):
        if not message:
            self.__ConnectionManager.sendMessage()
        else:
            self.__ConnectionManager.sendMessage(message, self.__gui.getChnlStr())

    def callTidyUpActivities(self):
        if not self.__activityController:
            return
        reply = self.__activityController.doTidyUp(confirm_entry=(self.__gui.JoinReplyVar.get() == 1))

        if reply:
            self.sendMessage(reply)

    def recvBuff(self):
        return self.__ConnectionManager.recvBuff()

    def isConnectionHealthy(self):
        return self.__ConnectionManager.isConnected() and self.__gui.isConnectActive()

    def loggingActive(self, mode: Modes, boolean: typing.Union[bool, None] = None) -> bool:
        if not self.__activityController:
            return False
        if boolean is not None:
            # Disable all activities when there is no connection, the stop is set for the active mode, or None is selected
            if (
                not self.isConnectionHealthy()
                or (not boolean and self.__activityController.isActivityEnabled(mode))
                or (mode == Modes.NONE and boolean)
            ):
                self.__activityController.selectActivity(Modes.NONE)
                return False
            if boolean:
                reply = self.__activityController.selectActivity(
                    mode, confirm_entry=(self.__gui.JoinReplyVar.get() == 1)
                )
                if reply:
                    self.sendMessage(reply)
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
            lineReply = False
            readbuffer = self.recvBuff()
            if readbuffer:
                temp = str.split(readbuffer, "\n")
                readbuffer = temp.pop()
                for line in temp:
                    # print(line)
                    lineReply = self.processLine(line)
            if not readbuffer or not lineReply:
                self.callTidyUpActivities()

    def mainloop(self):
        if self.__gui:
            self.__gui.mainloop()
