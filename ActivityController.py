"""Activity controller"""
import typing
import UserList
import Tools
import ActivityBase
import HelloActivity
import PoolActivity
import ListBoxInterface


class ActivityController:
    """Coordinates the different activites available on the bot"""

    __userlist: UserList.UserList
    __activitylist: dict[Tools.Modes, ActivityBase.ActivityBase]
    __anyenabled: bool

    def __init__(self, _chatbox: ListBoxInterface.ListBoxInterface) -> None:
        self.__userlist = UserList.UserList(_chatbox)
        # Instantiate all our activities
        self.__activitylist = {
            Tools.Modes.HELLO: HelloActivity.HelloActivity(self.__userlist),
            Tools.Modes.POOL: PoolActivity.PoolActivity(self.__userlist),
        }
        self.__anyenabled = False

    def select_activity(self, _activity: Tools.Modes, **kwargs) -> str:
        """Enables the specified activity.

        Args:
            _activity (Tools.Modes)

        Returns:
            str: reply to chat.
        """
        for _, act in self.__activitylist.items():
            act.disable()

        if _activity in self.__activitylist:
            self.__anyenabled = True
            return self.__activitylist[_activity].enable(**kwargs)
        else:
            self.__anyenabled = False
        return ""

    def is_activity_enabled(self, _activity: Tools.Modes = Tools.Modes.NONE) -> bool:
        """Checks if a specific activity is enabled. NONE checks if ANY activity is enabled.

        Args:
            _activity (Tools.Modes, optional): Activity specified. Defaults to Tools.Modes.NONE.

        Returns:
            bool: True if the activity is enabled; otherwise; False.
        """
        if _activity == Tools.Modes.NONE:
            return self.__anyenabled
        if _activity in self.__activitylist:
            return self.__activitylist[_activity].is_active()
        return False

    def do_action(self, user: str, message: str, **kwargs) -> typing.Union[str, bool]:
        """Calls the matching command for the activity enabled.

        Args:
            user (str): username
            message (str): user's message

        Returns:
            typing.Union[str, bool]: str reply to chat, True if successful; otherwise, False.
        """
        if not self.__anyenabled:
            return ""
        for _, act in self.__activitylist.items():
            if act.is_active():
                return act.do_command(user, message, **kwargs)
        return ""

    def do_tidy_up(self, **kwargs) -> str:
        """Calls the activity enabled to tidy up.

        Returns:
            str: reply to chat.
        """
        if not self.__anyenabled:
            return ""
        for _, act in self.__activitylist.items():
            if act.is_active():
                return act.do_tidy_up(**kwargs)
        return ""

    def delete_list(self) -> None:
        """Clears out the chatters list."""
        self.__userlist.delete_list()
