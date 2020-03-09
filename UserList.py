import os
from DictLabel import *

class UserList():
    __names = []
    __saveFilevar = ""

    def addToList(self, user, message, listChatters, ignoreList, fileVar):
        if not listChatters:
            return
        if user and message:
            if not (user in self.__names) and not (user in ignoreList):
                listChatters.insert(END, user + ":   " + message)
                self.__names.append(user)
                if fileVar and (not self.__saveFilevar or self.__saveFilevar != fileVar):
                    self.__saveFilevar = fileVar
                if self.__saveFilevar:
                    if len(self.__names) == 1:
                        try:
                            os.remove(self.__saveFilevar)
                        except:
                            pass
                    try:
                        if os.path.isfile(self.__saveFilevar):
                            recordFile = open(self.__saveFilevar, 'a')
                        elif self.__saveFilevar:
                            recordFile = open(self.__saveFilevar, 'w')
                            
                        if recordFile:
                            recordFile.write(user+"\n")
                            recordFile.close()
                    except:
                        pass

    def removeFromList(self, user, listChatters, fileVar):
        if not listChatters:
            return
        if user:
            if not (user in self.__names):
                listChatters... ## check and remove things 

    def deleteList(self):
        self.__names = []
        if os.path.isfile(self.__saveFilevar):
            os.remove(self.__saveFilevar)

    def size(self):
        return len(self.__names)