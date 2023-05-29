import Application

def twitchBot():       
    app.chatCheck()
    app.after(750, twitchBot)

app = Application.Application()
app.after(250, twitchBot)
app.mainloop()
