import os
from DictLabel import *
import ListBoxInterface

spaceString = ":   "


class UserList:
    __names = []
    __saveFilevar = ""

    def __init__(self, _guiList: ListBoxInterface.ListBoxInterface) -> None:
        self.__listOfChatters = _guiList

    def addToList(self, user, message) -> str:
        if not self.__listOfChatters:
            return ""
        if user and message:
            if not (user in self.__names) and not (user in self.__listOfChatters.getIngoreStr()):
                listOfChatters = self.__listOfChatters.getChatBox()
                if listOfChatters is None:
                    return ""
                listOfChatters.add_item(user + spaceString + message)
                self.__names.append(user)
                if self.__listOfChatters.isFileSaveActive():
                    fileVar = self.__listOfChatters.getSaveStr()
                    if fileVar and (not self.__saveFilevar or self.__saveFilevar != fileVar):
                        self.__saveFilevar = fileVar
                    if self.__saveFilevar:
                        if len(self.__names) == 1:
                            try:
                                os.remove(self.__saveFilevar)
                            except:
                                pass
                        try:
                            recordFile = ""
                            if os.path.isfile(self.__saveFilevar):
                                recordFile = open(self.__saveFilevar, "a")
                            elif self.__saveFilevar:
                                recordFile = open(self.__saveFilevar, "w")

                            if recordFile:
                                recordFile.write(user + "\n")
                                recordFile.close()
                        except:
                            pass
        return ""

    def deleteList(self):
        self.__names = []
        if os.path.isfile(self.__saveFilevar):
            os.remove(self.__saveFilevar)

    def isInList(self, _user: str):
        return _user in self.__names

    def size(self) -> int:
        return len(self.__names)

    def removeUser(self, user) -> str:
        if user in self.__names:
            index = self.__names.index(user)
            return self.selectEntry(index)
        return ""

    def selectEntry(self, _num) -> str:
        listOfChatters = self.__listOfChatters.getChatBox()

        if _num < self.size() and listOfChatters is not None:
            message = listOfChatters.get(_num)
            listOfChatters.delete(_num)
            del self.__names[_num]
            return message
        return ""

    def isHost(self, _user) -> bool:
        return _user.lower() == self.__listOfChatters.getChnlStr().lower()
