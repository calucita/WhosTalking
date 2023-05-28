import ListBox_Custom
import typing


class ListBoxInterface:
    ListChatters: typing.Union[ListBox_Custom.ListBox_Custom, None]

    def getIngoreStr(self) -> str:
        return ""

    def getSaveStr(self) -> str:
        return ""

    def getChatBox(self) -> typing.Union[ListBox_Custom.ListBox_Custom, None]:
        return self.ListChatters

    def getChnlStr(self) -> str:
        return ""
