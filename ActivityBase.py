"""Base class for activities"""
import typing
import UserList


class ActivityBase:
    """Base class for set of commands or 'activities', such as hello, or join pools."""

    def __init__(self, chatbox: UserList.UserList, cmdlist: typing.Union[dict, None] = None):
        if not cmdlist or len(cmdlist) == 0:
            raise ValueError("No commands added to" + str(type(self)))
        self.__commandlist = cmdlist
        self._enabled = False
        self._userlist = chatbox

    def enable(self, **kwargs) -> str:
        """Enables the activity

        Returns:
            str: a message to be relayed to chat
        """
        self._enabled = True
        return self.do_on_enable(**kwargs)

    def do_on_enable(self, **_kwargs) -> str:
        """Triggered when the activity is first enabled.

        Returns:
            str: a message to be relayed to chat.
        """
        return ""

    def disable(self):
        """Ends the activity"""
        self._enabled = False

    def is_active(self) -> bool:
        """Is the activity enabled.

        Returns:
            bool: True if enabled; otherwise False.
        """
        return self._enabled

    def do_command(self, user: str, message: str, **kwargs) -> typing.Union[str, bool]:
        """Performs the selected command for the user.

        Args:
            user (str): username
            message (str): message in chat

        Returns:
            typing.Union[str, bool]: reply for chat, or True if success; otherwise, False.
        """
        if "" in self.__commandlist:
            split_m = ""
        else:
            split_m = str.split(message)[0]
        if split_m in self.__commandlist:
            temp = self.__commandlist[split_m](user, message, **kwargs)
            return temp
        return ""

    def do_tidy_up(self, **_kwargs) -> str:
        """Wraps up any pending tasks"""
        return ""

    def add_to_list(self, user, message):
        """Adds the user to the user list.

        Args:
            user (_type_): username
            message (_type_): message in chat
        """
        if not self._enabled:
            return
        self._userlist.add_to_list(user, message)
