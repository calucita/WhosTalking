import UserList
import typing


class ActivityBase:
    """Base class for set of commands or 'activities', such as hello, or join pools."""

    def __init__(self, _chatBox: UserList.UserList, _cmdList: dict = {}):
        self.__CommandList = _cmdList
        if len(self.__CommandList) == 0:
            raise Exception("No commands added to" + str(type(self)))
        self._enabled = False
        self._UserList = _chatBox

    def enable(self, _activityBool: bool = False) -> str:
        """
        Enables the activity
        _activityBool: argument for the activity.
        returns: reply to chat.
        """
        self._enabled = True
        return self.doOnEnable(_activityBool)

    def doOnEnable(self, _activityBool: bool = False) -> str:
        return ""

    def disable(self):
        self._enabled = False

    def isActive(self) -> bool:
        return self._enabled

    def doCommand(self, user: str, message: str) -> typing.Union[str, bool]:
        for command in self.__CommandList:
            if message.lower().startswith(command):
                return self.__CommandList[command](user, message)

        return ""

    def doTidyUp(self, _activityBool: bool = False) -> str:
        """Wraps up any pending tasks"""
        return ""

    def addToList(self, user, message):
        if not self._enabled:
            return
        self._UserList.addToList(user, message)
