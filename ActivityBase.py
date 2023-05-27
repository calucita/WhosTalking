import UserList


class ActivityBase:
    """Base class for set of commands or 'activities', such as hello, or join pools."""

    def __init__(self, _chatBox: UserList.UserList, _cmdList: dict = {}):
        self.__CommandList = _cmdList
        if len(self.__CommandList) == 0:
            raise Exception("No commands added to" + str(type(self)))
        self._enabled = False
        self._UserList = _chatBox

    def enable(self) -> str:
        self._enabled = True
        return self.doOnEnable()

    def doOnEnable(self) -> str:
        return ""

    def disable(self):
        self._enabled = False

    def isActive(self) -> bool:
        return self._enabled

    def doCommand(self, user: str, message: str) -> str:
        for command in self.__CommandList:
            if message.lower().startswith(command):
                return self.__CommandList[command](user, message)

        return ""

    def addToList(self, user, message):
        if not self._enabled:
            return
        self._UserList.addToList(user, message)
