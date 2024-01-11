"""Basic interface for GUI callers."""
import typing
from Tools import Modes


class GUICallerInterface:
    """Interface for classes that need to call the GUI."""

    def logging_active(self, mode: Modes, connectionstate: typing.Union[bool, None] = None) -> bool:
        """Determines if a chat logging mode is enabled.

        Args:
            mode (Modes): logging mode to test
            connectionstate (typing.Union[bool, None], optional): Status of the connection. Defaults to None.

        Returns:
            bool: True if mode active; otherwise False.
        """
        raise NotImplementedError

    def pick_user(self):
        """Choose a user from the list, if possible."""
        raise NotImplementedError

    def delete_list(self):
        """Delete the user list."""
        raise NotImplementedError

    def set_connection(self, connect: bool) -> None:
        """Changes the status of the connection

        Args:
            connect (bool): True if connected; otherwise False.
        """
        raise NotImplementedError
