import Application

def twitchBot():       
    app.chatCheck()
    app.after(1000, twitchBot)

app = Application.Application()
app.after(1000, twitchBot)
app.mainloop()
