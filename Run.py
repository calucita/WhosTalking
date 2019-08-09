import string
from Read import getUser, getMessage

import Application

def twitchBot():       
    if app.isConnectionHealthy():
        readbuffer = app.recvBuff()
        if readbuffer:
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()
            for line in temp:
                if "PING" in line:
                    app.sendMessage()
                    break
                app.addToList(getUser(line), getMessage(line))

    app.after(1000, twitchBot)
			
app = Application.Application()
app.after(1000, twitchBot)
app.mainloop()
