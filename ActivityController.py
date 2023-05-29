import UserList
import Tools
import HelloActivity
import PoolActivity
import ListBoxInterface
import typing


class ActivityController:
    """Coordinates the different activites available on the bot"""

    def __init__(self, _chatbox: ListBoxInterface.ListBoxInterface) -> None:
        self.__UserList = UserList.UserList(_chatbox)
        # Instantiate all our activities
        self.__ActivityList = {
            Tools.Modes.HELLO: HelloActivity.HelloActivity(self.__UserList),
            Tools.Modes.POOL: PoolActivity.PoolActivity(self.__UserList),
        }
        self.__anyEnabled = False

    def selectActivity(self, _activity: Tools.Modes, **kwargs) -> str:
        for act in self.__ActivityList:
            self.__ActivityList[act].disable()

        if _activity in self.__ActivityList:
            self.__anyEnabled = True
            return self.__ActivityList[_activity].enable(**kwargs)
        else:
            self.__anyEnabled = False
        return ""

    def isActivityEnabled(self, _activity: Tools.Modes = Tools.Modes.NONE) -> bool:
        if _activity == Tools.Modes.NONE:
            return self.__anyEnabled
        if _activity in self.__ActivityList:
            return self.__ActivityList[_activity].isActive()
        return False

    def doAction(self, user: str, message: str) -> typing.Union[str, bool]:
        if not self.__anyEnabled:
            return ""
        for act in self.__ActivityList:
            if self.__ActivityList[act].isActive():
                return self.__ActivityList[act].doCommand(user, message)
        return ""

    def doTidyUp(self, **kwargs) -> str:
        if not self.__anyEnabled:
            return ""
        for act in self.__ActivityList:
            if self.__ActivityList[act].isActive():
                return self.__ActivityList[act].doTidyUp(**kwargs)
        return ""

    def deleteList(self) -> None:
        self.__UserList.deleteList()
