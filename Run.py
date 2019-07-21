import string
from Read import getUser, getMessage
from Socket import sendMessage, recv_timeout

import GUI

def twitchBot():
    if not app.isConnected(app.connected):
        app.connectSocket()
        
    if app.logNames and app.isConnected():
        readbuffer = recv_timeout(app.socket)
        if readbuffer:
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()
            for line in temp:
                if "PING" in line:
                    sendMessage(app.socket, "PONG")
                    break
                user = getUser(line)
                message = getMessage(line)
                app.addToList(user, message)

    app.after(1000, twitchBot)
			
app = GUI.Application(GUI.Tk())
app.after(1000, twitchBot)
app.mainloop()
