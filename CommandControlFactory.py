class CommandControlFactory:
    __commandList: dict = {}

    def createControl(self, type):
        newControl = type.capitalize()
        return globals()[newControl]()

    def createFromCommand(self, command):
        if command in self.__commandList:
            return self.createControl(self.__commandList[command])
        return False

    def getAllCommands(self):
        return self.__commandList.keys()
