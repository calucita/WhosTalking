class CommandControlFactory():
    __commandList = {}

    def createControl(self, type):
        newControl = type.capitalize()
        return globals()[newControl]()

    def createFromCommand(self, command):
        if __commandList.has_key(command):
            return self.createControl(_commandList[command])
        return False

    def getAllCommands(self):
        return __commandList.keys()