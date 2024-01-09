"""Basic interface for list box"""
import typing
import CustomListBox


class ListBoxInterface:
    """Bare bones for a GUI needing a ListBox, and the classes interacting with it."""

    _listchatters: typing.Union[CustomListBox.CustomListBox, None]

    def get_ingore_str(self) -> str:
        """Retrieves the string of names to ignore in chat.

        Returns:
            str: comma separated string with names.
        """
        raise NotImplementedError

    def get_save_str(self) -> str:
        """Retrieves the path to save files to.

        Returns:
            str: file path.
        """
        raise NotImplementedError

    def get_chat_box(self) -> typing.Union[CustomListBox.CustomListBox, None]:
        """Retrieves the listbox GUI component.

        Returns:
            typing.Union[ListBox_Custom.ListBox_Custom, None]
        """
        return self._listchatters

    def get_chnl_str(self) -> str:
        """Retrieves the connected channel's name.

        Returns:
            str: channel name.
        """
        raise NotImplementedError

    def is_file_save_active(self) -> bool:
        """Retrieves user set variable for file save option.

        Returns:
            bool: True if list should be saved to file; otherwise False.
        """
        raise NotImplementedError
