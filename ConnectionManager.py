"""Wraper for the local socket."""
import time
import typing
import ObserverPattern
import SocketLocal


class ConnectionManager:
    """Wrapper for the local socket for easier management of the connection."""

    __socket: typing.Union[SocketLocal.SocketLocal, None]
    __connected: bool
    __observer: ObserverPattern.ObserverPattern

    def __init__(self, observer: ObserverPattern.ObserverPattern) -> None:
        self.__socket = None
        self.__connected = False
        self.__observer = observer

    def __connect_socket(self, _name: str = "", _channel: str = "", _oauth: str = "") -> None:
        """Connect to twitch. Retries 3 times to avoid transient errors.

        Args:
            _name (str, optional): bot name. Defaults to "".
            _channel (str, optional): channel to connect to. Defaults to "".
            _oauth (str, optional): token. Defaults to "".
        """
        connectionerror = 2
        for _ in range(3):
            connectionerror = self.__retriable_connect(_name, _channel, _oauth)
            if not connectionerror:
                self.is_connected(connectionerror == 0, True, connectionerror)
                return
        self.is_connected(connectionerror == 0, True, connectionerror)

    def __retriable_connect(self, _name: str = "", _channel: str = "", _oauth: str = "") -> int:
        """Retriable connection call."""
        if self.__connected:
            return 0
        if self.__socket is None:
            self.__socket = SocketLocal.SocketLocal()
        if _oauth and _name and _channel:
            self.__socket.open_socket(str(_oauth), str(_name), str(_channel))
            connectionerror = self.__join_room(_name)
            if connectionerror:
                self.__socket = None
            return connectionerror
        return 2

    def is_connected(self, status: typing.Union[bool, None] = None, fromconnection=False, errorcode=0) -> bool:
        """Checks if the bot is connected.

        Args:
            status (typing.Union[bool, None]): is app connected
            fromconnection (bool, optional): is update connection manager. Defaults to False.
            errorcode (int, optional): Defaults to 0.

        Returns:
            bool: True if connected; otherwise False.
        """
        if status is not None:
            self.__observer.update(status, fromconnection, errorcode)
            self.__connected = status
        return self.__connected

    def set_connection(self, connect: bool, name: str = "", channel: str = "", oauth: str = "") -> None:
        """Connects or disconnects the bot.

        Args:
            connect (bool): Command to connect or disconnect.
            name (str, optional): Bot name. Defaults to "".
            channel (str, optional): Channel to connect to. Defaults to "".
            oauth (str, optional): token. Defaults to "".
        """
        if connect:
            self.__connect_socket(name, channel, oauth)
        else:
            if self.__socket:
                self.__socket.close()
                self.__socket = None
            self.is_connected(False)

    def recv_buff(self) -> str:
        """Retrieve a chat buffer.

        Returns:
            str: chat buffer.
        """
        if self.__socket:
            return self.__socket.recv_timeout()
        return ""

    def send_message(self, message: str = "", channel: str = "") -> None:
        """Sends a message to the specified channel.
        If no message is specified a pong reply is sent.

        Args:
            message (str, optional): Defaults to "'None'".
            channel (str, optional): Defaults to "".
        """
        if self.__socket is None:
            # move on...
            return
        if not message:
            self.__socket.send_message()
        else:
            self.__socket.send_message(message, channel)

    def __join_room(self, expecteduser: str) -> int:
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

                if expecteduser.lower() not in line.lower() and self.__socket:
                    self.__socket.close()
                    return 1

                if "failed" in line:
                    return 99

                if ":End of /NAMES list" in line:
                    # s.sendMessage("I'm here! I'm calu's bot :3")
                    return 0
        return 2
