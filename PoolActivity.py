import ActivityBase
import UserList
import random
import re
import DictLabel
import typing


class PoolActivity(ActivityBase.ActivityBase):
    def __init__(self, _chatBox: UserList.UserList):
        self.__joinCmd = "!join"
        cmds = {self.__joinCmd: self.joinQueue, "!leave": self.leaveQueue, "!pick": self.pickUser, "!joined": self.isInQueue}
        super().__init__(_chatBox, cmds)
        self.__announcement = DictLabel.txtNamePoolOpen
        self.__confirmEntry = False
        self.__pendingConfirmationsList = []
        self.__tidyCounter = 0

    def doOnEnable(self, **kwargs) -> str:
        if "confirm_entry" in kwargs:
            self.__confirmEntry = kwargs.pop("confirm_entry")
        self.__tidyCounter = 0
        return self.__announcement

    def doTidyUp(self, **kwargs) -> str:
        """Wraps up any pending tasks"""
        if "confirm_entry" in kwargs:
            self.__confirmEntry = kwargs.pop("confirm_entry")

        if not len(self.__pendingConfirmationsList):
            return ""
        if not self.__confirmEntry:
            self.__pendingConfirmationsList.clear()
        elif self.__tidyCounter < 3:
            self.__tidyCounter += 1
        else:
            reply = "Joined the pool: "
            for name in self.__pendingConfirmationsList:
                reply += str(name) + ", "
            reply = reply[:-2]
            self.__pendingConfirmationsList.clear()
            self.__tidyCounter = 0
            return reply
        return ""

    def joinQueue(self, _user: str, _message: str, **kwargs) -> typing.Union[str, bool]:
        regex_message = re.compile(self.__joinCmd, re.IGNORECASE)
        _message = regex_message.sub("", _message)
        if not self._UserList.isInList(_user):
            self.addToList(_user, _message)
            self.__pendingConfirmationsList.append(_user)
        else:
            reply = False
            if "reply" in kwargs:
                reply = kwargs.pop("reply")
            if reply:
                return self.isInQueue(_user)
        return True

    def leaveQueue(self, _user: str, _message: str, **kwargs) -> str:
        if self._UserList.isInList(_user):
            self._UserList.removeUser(_user)
            return "@" + _user + " has left the name pool"
        return ""

    def pickUser(self, _user: str, _message: str, **kwargs) -> str:
        if self._UserList.isHost(_user):
            if self._UserList.size() == 0:
                return "No one has joined yet... :( ... "

        chosen = self._UserList.selectEntry(random.randint(0, self._UserList.size() - 1))
        if chosen:
            chosen = chosen.split(":   ")
            user = chosen[0]
            message = chosen[1].strip()
            if len(chosen) == 2 and message:
                return "Winner! User: " + user + " with message " + message
            else:
                return "Winner! User: " + user
        return ""

    def isInQueue(self, _user: str, _message: str = "", **kwargs) -> str:
        message = self._UserList.getMessage(_user)
        if not message:
            return _user + " is not in the name pool."
        message = message.split(":   ")
        message = message[1].strip()
        if message:
            return _user + " is in the name pool, with message: " + message
        return _user + " is in the name pool"
