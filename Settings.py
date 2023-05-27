import keyring

# This is for windows... ... might generalize later...
from keyrings.alt import Windows

keyring.set_keyring(Windows.RegistryKeyring())

service = "Whostalking"
saveF = "saveFile"


def loadCredentials(app):
    fileName = getSaveFileFromKey()
    if fileName:
        app.SaveEntry.insert(0, fileName)
        app.SaveCheck.select()

    botto = keyring.get_password(service, service)
    if not botto:
        return

    app.NameEntry.insert(0, str(botto))
    channel = keyring.get_password(service, botto)
    if not channel:
        return

    app.ChannelEntry.insert(0, str(channel))
    oauth = keyring.get_password(service, botto + channel)
    if not oauth:
        return

    app.OauthEntry.insert(0, oauth)


def saveCredentials(app):
    keyring.set_password(service, service, app.NameEntry.get())
    keyring.set_password(service, app.NameEntry.get(), app.ChannelEntry.get())
    keyring.set_password(service, app.NameEntry.get() + app.ChannelEntry.get(), app.OauthEntry.get())


def saveFileInKey(saveFile):
    keyring.set_password(service, saveF, saveFile)


def getSaveFileFromKey():
    return keyring.get_password(service, saveF)
