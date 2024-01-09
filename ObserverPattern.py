"""Multipurpose observer pattern."""
import typing


class ObserverPattern:
    """Simplified observer interface."""

    def update(self, status: typing.Union[bool, None], fromconnection: bool = False, errorcode: int = 0) -> None:
        """Trigger update processes

        Args:
            status (typing.Union[bool, None]): is app connected
            fromconnection (bool, optional): is update from a connection manager. Defaults to False.
            errorcode (int, optional): Defaults to 0.
        """

        raise NotImplementedError
