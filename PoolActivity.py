"""Name pool activity"""

import typing
import random
import re
import DictLabel
import ActivityBase
import UserList


class PoolActivity(ActivityBase.ActivityBase):
    """Name pool activity, for volunteers to join and a random person to be picked."""

    def __init__(self, _chatBox: UserList.UserList):
        self.__joincmd = "!join"
        cmds = {self.__joincmd: self.join_queue, "!leave": self.leave_queue, "!pick": self.pick_user, "!joined": self.is_in_queue}
        super().__init__(_chatBox, cmds)
        self.__announcement = DictLabel.TXTNAMEPOOLOPEN
        self.__confirmentry = False
        self.__pendingconfirmationslist = []
        self.__tidycounter = 0

    def do_on_enable(self, **kwargs) -> str:
        if "confirm_entry" in kwargs:
            self.__confirmentry = kwargs.pop("confirm_entry")
        self.__tidycounter = 0
        return self.__announcement

    def do_tidy_up(self, **kwargs) -> str:
        """Wraps up any pending tasks"""
        if "confirm_entry" in kwargs:
            self.__confirmentry = kwargs.pop("confirm_entry")

        if len(self.__pendingconfirmationslist) == 0:
            return ""
        if not self.__confirmentry:
            self.__pendingconfirmationslist.clear()
        elif self.__tidycounter < 3:
            self.__tidycounter += 1
        else:
            reply = "Joined the pool: "
            for name in self.__pendingconfirmationslist:
                reply += str(name) + ", "
            reply = reply[:-2]
            self.__pendingconfirmationslist.clear()
            self.__tidycounter = 0
            return reply
        return ""

    def join_queue(self, _user: str, _message: str, **kwargs) -> typing.Union[str, bool]:
        """Join command trigger.

        Args:
            _user (str): username
            _message (str): user's message in chat

        Returns:
            typing.Union[str, bool]: str if reply needed, True if successful; otherwise, False.
        """
        regex_message = re.compile(self.__joincmd, re.IGNORECASE)
        _message = regex_message.sub("", _message)
        if not self._userlist.is_in_list(_user):
            self.add_to_list(_user, _message)
            self.__pendingconfirmationslist.append(_user)
        else:
            reply = False
            if "reply" in kwargs:
                reply = kwargs.pop("reply")
            if reply:
                return self.is_in_queue(_user)
        return True

    def leave_queue(self, _user: str, _message: str, **_kwargs) -> str:
        """Leave the pool command.

        Args:
            _user (str): username to leave the pool.
            _message (str): user's message in chat.

        Returns:
            str: str if reply needed, True if successful; otherwise, False.
        """
        if self._userlist.is_in_list(_user):
            self._userlist.remove_user(_user)
            return "@" + _user + " has left the name pool"
        return ""

    def pick_user(self, _user: str, _message: str, **_kwargs) -> str:
        """Pick user from the pool command.

        Args:
            _user (str): username requesting the pick.
            _message (str): user's message in chat.

        Returns:
            str: str if reply needed, True if successful; otherwise, False.
        """
        if self._userlist.is_host(_user):
            if self._userlist.size() == 0:
                return "No one has joined yet... :( ... "

        chosen = self._userlist.select_entry(random.randint(0, self._userlist.size() - 1))
        if chosen:
            chosen = chosen.split(":   ")
            user = chosen[0]
            message = chosen[1].strip()
            if len(chosen) == 2 and message:
                return "Winner! User: " + user + " with message " + message
            else:
                return "Winner! User: " + user
        return ""

    def is_in_queue(self, _user: str, _message: str = "", **_kwargs) -> str:
        """Checks if the user is already in the pool.

        Args:
            _user (str): username requesting the check.
            _message (str): user's message in chat.

        Returns:
            str: reply to the user.
        """
        message = self._userlist.get_message(_user)
        if not message:
            return _user + " is not in the name pool."
        message = message.split(":   ")
        message = message[1].strip()
        if message:
            return _user + " is in the name pool, with message: " + message
        return _user + " is in the name pool"
