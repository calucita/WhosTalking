""""Main() runner of the bot."""
import Application


def twitch_bot():
    """What to do in the infinite loop."""
    app.chat_check()
    app.after(500, twitch_bot)


app = Application.Application()
app.after(250, twitch_bot)
app.mainloop()
