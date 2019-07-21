import os
import keyring
# This is for windows... ... ming generalize later... 
from keyrings.alt import Windows
keyring.set_keyring(Windows.RegistryKeyring())

fileName=os.getcwd()+"\\credentials.txt"
service="Whostalking"

def loadCredentials(app):
    # if this file exists, let's fix it
    if os.path.isfile(fileName):
        try:
            
            creds = open(fileName, 'r')
            for line in creds:
                if "PASS" in line:
                    loadMsg(app.OauthEntry, line)
                elif "IDENT" in line:
                    loadMsg(app.NameEntry, line)
                elif "CHANNEL" in line:
                    loadMsg(app.ChannelEntry, line)
            creds.close()
            os.remove(fileName)
            saveCredentials(app)
        except:
            pass
    else:
        botto = keyring.get_password(service, service)
        if not botto:
            return

        app.NameEntry.insert(0, str(botto))
        channel = keyring.get_password(service, botto)
        if not channel:
            return
        
        app.ChannelEntry.insert(0, str(channel))
        oauth = keyring.get_password(service, botto+channel)
        if not oauth:
            return
        
        app.OauthEntry.insert(0, oauth)
    
    
def saveCredentials(app):
    keyring.set_password(service, service, app.NameEntry.get())
    keyring.set_password(service, app.NameEntry.get(), app.ChannelEntry.get())
    keyring.set_password(service, app.NameEntry.get()+app.ChannelEntry.get(), app.OauthEntry.get())
    
def loadMsg(entry, line):
    entry.delete(0, 'end')
    entry.insert(0, line.split("=")[1])

