import ActivityBase
import UserList
import random
import re
import DictLabel


class PoolActivity(ActivityBase.ActivityBase):
    def __init__(self, _chatBox: UserList.UserList):
        self.__joinCmd = "!join"
        cmds = {self.__joinCmd: self.joinQueue, "!leave": self.leaveQueue, "!pick": self.pickUser}
        super().__init__(_chatBox, cmds)
        self.__announcement = DictLabel.txtNamePoolOpen

    def doOnEnable(self) -> str:
        return self.__announcement

    def joinQueue(self, _user, _message) -> str:
        regex_message = re.compile(self.__joinCmd, re.IGNORECASE)
        _message = regex_message.sub("", _message)
        self.addToList(_user, _message)
        return ""

    def leaveQueue(self, _user, _message) -> str:
        if self._UserList.isInList(_user):
            self._UserList.removeUser(_user)
            return "@" + _user + " has left the name pool"
        return ""

    def pickUser(self, _user, _message) -> str:
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
