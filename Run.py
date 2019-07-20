import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage, recv_timeout
from Initialize import joinRoom
from Settings import saveCredentials
import GUI

def twitchBot():
    app.isConnected(app.connected)
    if not app.connected and app.toggle_btn.config('relief')[-1] == 'sunken':
        if (app.OauthEntry.get() and app.NameEntry.get() and app.ChannelEntry.get()):
            app.socket = openSocket(str(app.OauthEntry.get()), str(app.NameEntry.get()), str(app.ChannelEntry.get()))
            app.connected = joinRoom(app.socket)
            if app.connected:
                saveCredentials(app)
            else:
                app.ChannelLabel.delete(0, 'end')
                app.ChannelLabel.insert('Error')

    if app.connected and app.toggle_btn.config('relief')[-1] == 'raised':
        app.socket.close()
        app.connected = False
    if app.logNames:
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
