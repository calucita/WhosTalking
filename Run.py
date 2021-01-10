import Application

def twitchBot():       
    if app.isConnectionHealthy():
        readbuffer = app.recvBuff()
        if readbuffer:
            temp = str.split(readbuffer, "\n")
            readbuffer = temp.pop()
            for line in temp:
                #print(line)
                if "PING" in line:
                    app.sendMessage()
                    break
                app.processLine(line)

    app.after(1000, twitchBot)

app = Application.Application()
app.after(1000, twitchBot)
app.mainloop()
