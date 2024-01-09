"""twitch specific socket wrapper."""
import typing
import socket
import time

HOST = "irc.twitch.tv"
PORT = 6667


class SocketLocal:
    """Socket wrapper for twitch connection."""

    __socket: typing.Union[socket.socket, None] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open_socket(self, pas: str, ident: str, channel: str) -> None:
        """Opens a socket to twitch.

        Args:
            pas (str): Token
            ident (str): botname
            channel (str): channel to connect to
        """
        if not self.__socket:
            self.__socket = socket.socket()
            self.__socket.connect((HOST, PORT))
            self.__send("PASS " + pas + "\r\n")
            self.__send("NICK " + ident + "\r\n")
            self.__send("JOIN #" + channel + "\r\n")

    def send_message(self, message: str = "PONG :tmi.twitch.tv\r\n", channel: str = "") -> None:
        """Use the existing socket to send a message

        Args:
            message (str, optional): Defaults to "PONG :tmi.twitch.tv\r\n".
            channel (str, optional): Defaults to "".
        """
        if not channel:
            self.__send(message)
            return
        self.__send("PRIVMSG #" + channel + " :" + message + "\r\n")

    def recv_timeout(self, timeout: float = 0.250) -> str:
        """Receive strings with a timeout

        Args:
            timeout (float, optional): Defaults to 0.250.

        Returns:
            str: buffer received.
        """
        data = ""
        # make socket non blocking
        if self.__socket:
            self.__socket.setblocking(False)

        begin = time.time()
        while True:
            if data:
                break

            # if you got no data at all bail out
            elif time.time() - begin > float(timeout):
                break

            try:
                if self.__socket:
                    data = self.__socket.recv(1024).decode()
            except UnicodeDecodeError:
                pass

        return data

    def __send(self, message):
        if self.__socket and message:
            self.__socket.send(str.encode(message))

    def close(self) -> None:
        """Close the socket - Disconnect"""
        if self.__socket:
            self.__socket.close()
