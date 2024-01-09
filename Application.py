"""Module for the main application class."""
import typing
import GUI
import Settings
import ConnectionManager
import ObserverPattern
import ActivityController
import GUICallerInterface
import TwitchOauth
from Tools import Modes
from Read import getUser, getMessage


class Application(ObserverPattern.ObserverPattern, GUICallerInterface.GUICallerInterface):
    """Main application class"""

    __activitycontroller: typing.Union[ActivityController.ActivityController, None]

    def __init__(self):
        self.__gui = GUI.GUI(self)
        Settings.loadSavefile(self.__gui)
        Settings.loadCredentials(self.__gui.settings)
        self.__connectionmanager = ConnectionManager.ConnectionManager(self)
        self.__activitycontroller = ActivityController.ActivityController(self.__gui)

    def process_line(self, line: str) -> bool:
        """Processes a single line of chat

        Args:
            line (str): chat line

        Returns:
            bool: True if user chat, otherwise False.
        """
        if "PING :tmi.twitch.tv" in line:
            self.send_message()
            return False

        if self.__activitycontroller and self.__activitycontroller.isActivityEnabled():
            reply = self.call_activities(getUser(line), getMessage(line))

            if Settings.getSaveFileFromKey() != self.__gui.getSaveStr():
                Settings.saveFileInKey(self.__gui.getSaveStr())

            return reply
        return False

    def pick_user(self):
        self.call_activities(str(self.__gui.getChnlStr()), "!pick")

    def call_activities(self, user: str, message: str) -> bool:
        """Calls activity (queue) actions on a user message

        Args:
            user (str): user
            message (str): message

        Returns:
            bool: True if succeeded; otherwise False.
        """
        if not self.__activitycontroller:
            return False
        reply = self.__activitycontroller.doAction(user, message, reply=(self.__gui.settings.JoinReplyVar.get() == 1))

        if isinstance(reply, str):
            self.send_message(reply)
            return True
        if reply is True:
            return True
        return False

    def send_message(self, message: typing.Union[None, str] = None) -> None:
        """Send a message to a twitch chat.
        If no message is specified, it replies to the ping-pong heartbeat.

        Args:
            message (typing.Union[None, str], optional): Defaults to None.
        """
        if not message:
            self.__connectionmanager.sendMessage()
        else:
            self.__connectionmanager.sendMessage(message, self.__gui.getChnlStr())

    def call_tidyup_activities(self) -> None:
        """Calls back to the activities to wrapup any pending actions."""
        if not self.__activitycontroller:
            return
        reply = self.__activitycontroller.doTidyUp(confirm_entry=(self.__gui.settings.JoinReplyVar.get() == 1))

        if reply:
            self.send_message(reply)

    def recv_buff(self) -> str:
        """Retrieve message buffer from the connection manager.

        Returns:
            str: chat buffer.
        """
        return self.__connectionmanager.recvBuff()

    def is_connection_healthy(self) -> bool:
        """Checks if the connection is healthy.

        Returns:
            bool: True if connected; otherwise False.
        """
        return self.__connectionmanager.isConnected() and self.__gui.isConnectActive()

    def logging_active(self, mode: Modes, connectionstate: typing.Union[bool, None] = None) -> bool:
        if not self.__activitycontroller:
            return False
        if connectionstate is not None:
            # Disable all activities when there is no connection, the stop is set for the active mode,
            # or None is selected
            if (
                not self.is_connection_healthy()
                or (not connectionstate and self.__activitycontroller.isActivityEnabled(mode))
                or (mode == Modes.NONE and connectionstate)
            ):
                self.__activitycontroller.selectActivity(Modes.NONE)
                return False
            if connectionstate:
                reply = self.__activitycontroller.selectActivity(mode, confirm_entry=(self.__gui.settings.JoinReplyVar.get() == 1))
                if reply:
                    self.send_message(reply)
                if Settings.getSaveFileFromKey() != self.__gui.getSaveStr():
                    Settings.saveFileInKey(self.__gui.getSaveStr())

        return self.__activitycontroller.isActivityEnabled(mode)

    def delete_list(self) -> None:
        if self.__activitycontroller:
            self.__activitycontroller.deleteList()

    def set_connection(self, _connect: bool) -> None:
        if not self.__gui.settings.OauthVar.get():
            oauth = TwitchOauth.TwitchOauth()
            val = oauth.authenticate()
            if not val or val == "  ":
                self.update(False)
                return
            self.__gui.settings.OauthVar.set("oauth:" + val)

        self.__connectionmanager.setConnection(
            _connect,
            str(self.__gui.settings.NameVar.get()),
            str(self.__gui.settings.ChannelVar.get()),
            str(self.__gui.settings.OauthVar.get()),
        )

    def update(self, status: bool, fromconnection=False, errorcode=0) -> None:
        self.__gui.setConnectButton(status, errorcode, fromconnection)
        if status:
            Settings.saveCredentials(self.__gui.settings)

    def after(self, time: int, method):
        """Call GUI function once after given time.

        Args:
            time (int): in milliseconds
            method (_type_): function to run
        """
        if self.__gui:
            self.__gui.after(time, method)

    def chat_check(self) -> None:
        """Periodic check of the connection and twitch chat."""
        if self.is_connection_healthy():
            linereply = False
            readbuffer = self.recv_buff()
            if readbuffer:
                temp = str.split(readbuffer, "\n")
                readbuffer = temp.pop()
                for line in temp:
                    # print(line)
                    linereply = self.process_line(line)
            if not readbuffer or not linereply:
                self.call_tidyup_activities()

    def mainloop(self) -> None:
        """Wrapper for the GUI mainloop call."""
        if self.__gui:
            self.__gui.mainloop()
