import typing
from Tools import Modes


class GUICallerInterface:
    def loggingActive(self, mode: Modes, boolean: typing.Union[bool, None] = None) -> bool:
        return False

    def pickUser(self):
        pass

    def deleteList(self):
        pass

    def setConnection(self, _connect: bool) -> None:
        pass
