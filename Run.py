import Application


def twitchBot():
    app.chat_check()
    app.after(500, twitchBot)


app = Application.Application()
app.after(250, twitchBot)
app.mainloop()
