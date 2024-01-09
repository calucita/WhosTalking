"""Welcome/hello activity"""
import ActivityBase
import UserList


class HelloActivity(ActivityBase.ActivityBase):
    """Hello Queue activity."""

    def __init__(self, _chatBox: UserList.UserList):
        cmds = {"": self.join_queue}
        super().__init__(_chatBox, cmds)

    def join_queue(self, user, message, **_kwargs) -> str:
        """Command wapper to add the user to the user list.

        Args:
            user (_type_): username
            message (_type_): message in chat

        Returns:
            str: empty string.
        """
        self.add_to_list(user, message)
        return ""
