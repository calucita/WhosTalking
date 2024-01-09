"""User list backend"""
import os
from DictLabel import *
import ListBoxInterface

SPACESTRING = ":   "


class UserList:
    """Handles the logic for the user list."""

    __names = []
    __savefilevar = ""

    def __init__(self, guilist: ListBoxInterface.ListBoxInterface) -> None:
        self.__listofchatters = guilist

    def add_to_list(self, user: str, message: str) -> str:
        """Adds a user and their chat message to the list.

        Args:
            user (str): username
            message (str): chat message

        Returns:
            str: reply to chat.
        """
        if not self.__listofchatters:
            return ""
        if user and message:
            if not (user in self.__names) and not user in self.__listofchatters.get_ingore_str():
                chatlist = self.__listofchatters.get_chat_box()
                if chatlist is None:
                    return ""
                chatlist.add_item(user + SPACESTRING + message)
                self.__names.append(user)
                if self.__listofchatters.is_file_save_active():
                    filevar = self.__listofchatters.get_save_str()

                    if filevar and (not self.__savefilevar or self.__savefilevar != filevar):
                        self.__savefilevar = filevar
                    if self.__savefilevar:
                        if len(self.__names) == 1:
                            try:
                                os.remove(self.__savefilevar)
                            except FileNotFoundError:
                                pass
                        try:
                            recordfile = ""
                            if os.path.isfile(self.__savefilevar):
                                recordfile = open(self.__savefilevar, "a")
                            elif self.__savefilevar:
                                recordfile = open(self.__savefilevar, "w")

                            if recordfile:
                                recordfile.write(user + "\n")
                                recordfile.close()
                        except FileExistsError:  # todo all other possible errors...
                            pass
        return ""

    def delete_list(self) -> None:
        """Deletes all the entries in the chat list."""
        self.__names.clear()
        if os.path.isfile(self.__savefilevar):
            os.remove(self.__savefilevar)

    def is_in_list(self, user: str) -> bool:
        """Checks if the specified user is in the chat list.

        Args:
            user (str): username

        Returns:
            bool: True if the user is in the list; otherwise, False.
        """
        return user in self.__names

    def get_message(self, user: str) -> str:
        """Retrieves the message submitted by a user in the chat list.

        Args:
            user (str): username

        Returns:
            str: message associated to the user. Empty if the user is not in the list.
        """
        if not self.is_in_list(user):
            return ""
        chatlist = self.__listofchatters.get_chat_box()
        if chatlist:
            return chatlist.get(self.__names.index(user))
        return ""

    def size(self) -> int:
        """Retrieves the length of the chat list.

        Returns:
            int:
        """
        return len(self.__names)

    def remove_user(self, user: str) -> str:
        """removes a pecified user from the list.

        Args:
            user (str): username

        Returns:
            str: message associated with the user. Empty str if the user is not in the list.
        """
        if user in self.__names:
            index = self.__names.index(user)
            return self.select_entry(index)
        return ""

    def select_entry(self, num: int) -> str:
        """Removes a record from the chat list given an index.

        Args:
            num (int): index to remove

        Returns:
            str: str: message associated with the user. Empty str if out of range.
        """
        chatlist = self.__listofchatters.get_chat_box()

        if num < self.size() and chatlist is not None:
            message = chatlist.get(num)
            chatlist.delete(num)
            del self.__names[num]
            return message
        return ""

    def is_host(self, user: str) -> bool:
        """Checks if the username provided is the chat's host.

        Args:
            user (str): username

        Returns:
            bool: True if the user is the channel owner; otherwise, False.
        """
        return user.lower() == self.__listofchatters.get_chnl_str().lower()
