import os
fileName=os.getcwd()+"\\credentials.txt"

def loadCredentials(app):
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
    except:
        pass
    
def saveCredentials(app):
    try:
        creds = open(fileName, 'w')
        creds.write("PASS="+str(app.OauthEntry.get())+"\n" + "IDENT="+str(app.NameEntry.get())+"\n" + "CHANNEL="+str(app.ChannelEntry.get())+"\n")
        creds.close()
    except:
        pass
    
def loadMsg(entry, line):
    entry.delete(0, 'end')
    entry.insert(0, line.split("=")[1])

