import tkinter
import typing


class ListBoxInterface:
    ListChatters: typing.Union[tkinter.Listbox, None]

    def getIngoreStr(self) -> str:
        return ""

    def getSaveStr(self) -> str:
        return ""

    def getChatBox(self) -> typing.Union[tkinter.Listbox, None]:
        return self.ListChatters

    def getChnlStr(self) -> str:
        return ""
