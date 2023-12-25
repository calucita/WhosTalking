import keyring
import typing

# This is for windows... ... might generalize later...
from keyrings.alt import Windows

keyring.set_keyring(Windows.RegistryKeyring())

service = "Whostalking"
saveF = "saveFile"


def loadSavefile(app):
    fileName = getSaveFileFromKey()
    if fileName:
        app.SaveEntry.insert(0, fileName)
        app.SaveCheck.select()


def getCredentials() -> typing.Union[dict, None]:
    credentials = {}
    botto = keyring.get_password(service, service)
    if not botto:
        return None

    credentials["bot"] = botto
    channel = keyring.get_password(service, botto)
    if not channel:
        return None

    credentials["channel"] = channel
    oauth = keyring.get_password(service, botto + channel)
    if not oauth:
        return None

    credentials["oauth"] = oauth
    return credentials


def loadCredentials(app):
    credentials = getCredentials()
    if not credentials:
        return
    app.NameVar.set(credentials["bot"])
    app.ChannelVar.set(credentials["channel"])
    app.OauthVar.set(credentials["oauth"])


def saveCredentials(app):
    if app.NameVar.get() and app.ChannelVar.get() and app.OauthVar.get():
        keyring.set_password(service, service, app.NameVar.get())
        keyring.set_password(service, app.NameVar.get(), app.ChannelVar.get())
        keyring.set_password(service, app.NameVar.get() + app.ChannelVar.get(), app.OauthVar.get())


def saveFileInKey(saveFile):
    keyring.set_password(service, saveF, saveFile)


def getSaveFileFromKey():
    return keyring.get_password(service, saveF)
