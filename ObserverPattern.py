import typing


class ObserverPattern:
    def update(self, status: typing.Union[bool, None], fromConnection=False, errorCode=0) -> None:
        pass
