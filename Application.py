"""Module for the main application class."""
import typing
from Tools import Modes
import GUI
import Settings
import ConnectionManager
import ObserverPattern
import ActivityController
import GUICallerInterface
import TwitchOauth


class Application(ObserverPattern.ObserverPattern, GUICallerInterface.GUICallerInterface):
    """Main application class"""

    def __init__(self):
        self.__gui = GUI.GUI(self)
        self.__credentials: Settings.CredentialsSettings = self.__gui.get_credentials()
        self.__credentials.load_data()
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

        def get_user(line):
            if ":" in line and "!" in line:
                separate = line.split(":", 2)
                user = separate[1].split("!", 1)[0]
                return user
            return ""

        def get_message(line):
            if ":" in line:
                separate = line.split(":", 2)
                if len(separate) > 2:
                    message = separate[2]
                    return message
            return ""

        if self.__activitycontroller and self.__activitycontroller.is_activity_enabled():
            reply = self.call_activities(get_user(line), get_message(line))
            self.__credentials.save_file_in_key()

            return reply
        return False

    def pick_user(self):
        self.call_activities(str(self.__gui.get_chnl_str()), "!pick")

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
        reply = self.__activitycontroller.do_action(user, message, reply=self.__gui.is_reply_active())

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
            self.__connectionmanager.send_message()
        else:
            self.__connectionmanager.send_message(message, self.__gui.get_chnl_str())

    def call_tidyup_activities(self) -> None:
        """Calls back to the activities to wrapup any pending actions."""
        if not self.__activitycontroller:
            return
        reply = self.__activitycontroller.do_tidy_up(confirm_entry=self.__gui.is_reply_active())

        if reply:
            self.send_message(reply)

    def recv_buff(self) -> str:
        """Retrieve message buffer from the connection manager.

        Returns:
            str: chat buffer.
        """
        return self.__connectionmanager.recv_buff()

    def is_connection_healthy(self) -> bool:
        """Checks if the connection is healthy.

        Returns:
            bool: True if connected; otherwise False.
        """
        return self.__connectionmanager.is_connected() and self.__gui.is_connection_active()

    def logging_active(self, mode: Modes, connectionstate: typing.Union[bool, None] = None) -> bool:
        if not self.__activitycontroller:
            return False
        if connectionstate is not None:
            # Disable all activities when there is no connection, the stop is set for the active mode,
            # or None is selected
            if (
                not self.is_connection_healthy()
                or (not connectionstate and self.__activitycontroller.is_activity_enabled(mode))
                or (mode == Modes.NONE and connectionstate)
            ):
                self.__activitycontroller.select_activity(Modes.NONE)
                return False
            if connectionstate:
                reply = self.__activitycontroller.select_activity(mode, confirm_entry=self.__gui.is_reply_active())
                if reply:
                    self.send_message(reply)
                self.__credentials.save_file_in_key()

        return self.__activitycontroller.is_activity_enabled(mode)

    def delete_list(self) -> None:
        if self.__activitycontroller:
            self.__activitycontroller.delete_list()

    def set_connection(self, connect: bool) -> None:
        if not self.__credentials.oauthvar.get():
            oauth = TwitchOauth.TwitchOauth()
            val = oauth.authenticate()
            if not val or val == "  ":
                self.update(False)
                return
            self.__credentials.oauthvar.set("oauth:" + val)

        self.__connectionmanager.set_connection(
            connect,
            str(self.__credentials.namevar.get()),
            str(self.__credentials.channelvar.get()),
            str(self.__credentials.oauthvar.get()),
        )

    def update(self, status: bool, fromconnection=False, errorcode=0) -> None:
        self.__gui.set_connect_button(status, errorcode, fromconnection)
        if status:
            self.__credentials.save_credentials()

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
