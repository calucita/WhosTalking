import string
from Read import getUser, getMessage

import GUI

def twitchBot():
    if not app.isConnected(app.connected):
        app.connectSocket()
        
    if app.logNames and app.isConnected():
        readbuffer = app.recvBuff()
        if readbuffer:
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()
            for line in temp:
                if "PING" in line:
                    app.sendMessage()
                    break
                user = getUser(line)
                message = getMessage(line)
                app.addToList(user, message)

    app.after(1000, twitchBot)
			
app = GUI.Application(GUI.Tk())
app.after(1000, twitchBot)
app.mainloop()
