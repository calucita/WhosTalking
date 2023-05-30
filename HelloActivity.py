import ActivityBase
import UserList


class HelloActivity(ActivityBase.ActivityBase):
    def __init__(self, _chatBox: UserList.UserList):
        cmds = {"": self.joinQueue}
        super().__init__(_chatBox, cmds)

    def joinQueue(self, user, message) -> str:
        self.addToList(user, message)
        return ""
