from Tkinter import *
from Socket import openSocket
from Initialize import joinRoom
from Settings import loadCredentials, saveCredentials

class Application(Frame):
    connected = False
    logNames = False
    socket = ''
    names = []
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Who\'s talking")
        self.master.geometry('350x450')
        self.create_widgets()
        loadCredentials(self)
        self.pack()
        

    def create_widgets(self):
        
        # labels :)
        self.NameLabel =Label(self, text="Bot name")
        self.NameLabel.grid(column=1, row=1, sticky=W)
        self.OauthLabel =Label(self, text="OAUTH token")
        self.OauthLabel.grid(column=1, row=2, sticky=W)
        self.ChannelLabel =Label(self, text="Channel name")
        self.ChannelLabel.grid(column=1, row=3, sticky=W)
        self.ConnectLabel =Label(self, text="Not Connected", fg="red")
        self.ConnectLabel.grid(column=2, row=4)
        self.ListLabel =Label(self, text="\nList of chatters")
        self.ListLabel.grid(column=2, row=5)
        self.IgnoreLabel =Label(self, text="\nIgnore")
        self.IgnoreLabel.grid(column=1, row=7)

        # text boxes
        self.NameEntry =Entry(self, width=35)
        self.NameEntry.grid(column=2, row=1, sticky=W)
        self.OauthEntry =Entry(self, width=35, show="*")
        self.OauthEntry.grid(column=2, row=2, sticky=W)
        self.ChannelEntry =Entry(self, width=35)
        self.ChannelEntry.grid(column=2, row=3, sticky=W)
        self.IgnoreEntry =Entry(self, width=35)
        self.IgnoreEntry.grid(column=2, row=7, sticky=W+S)

        # Buttons
        self.ButtonFrame =Frame(self)
        self.ButtonFrame.grid(column=1, row=6)
        self.Start =Button(self.ButtonFrame, width=5, text="Start", command=self.onStart)
        self.Start.grid(column=1, row=1)
        self.Stop =Button(self.ButtonFrame, width=5, text="Stop", command=self.onStop)
        self.Stop.grid(column=1, row=2)
        self.Clear =Button(self.ButtonFrame, width=5, text="Clear", command=self.deleteList)
        self.Clear.grid(column=1, row=4)

        # Toggle connection
        self.toggle_btn = Button(self, text="Connect", width=12, relief="raised", command=self.toggle)
        self.toggle_btn.grid(column=1, row=4)

        # List box
        self.ListChatters =Listbox(self, height=15, yscrollcommand=Scrollbar(self).set)
        self.ListChatters.grid(column=2, row=6, sticky=W+E+N+S)

    def addToList(self, user, message):
        if user and message:
            if not (user in self.names) and not (user in self.IgnoreEntry.get()):
                self.ListChatters.insert(END, user + ": " + message)
                self.names.append(user)

    def deleteList(self):
        self.ListChatters.delete(0,END)
        self.names = []

    def onStart(self):
        if self.isConnected():
            self.logNames = True
            self.Start.config(relief="sunken")
            self.Stop.config(relief="raised")
        
    def onStop(self):
        self.logNames = False
        self.Start.config(relief="raised")
        self.Stop.config(relief="sunken")

    def connectSocket(self):
         if not self.isConnected() and self.toggle_btn.config('text')[-1] == 'Disconnect':
            if (self.OauthEntry.get() and self.NameEntry.get() and self.ChannelEntry.get()):
                self.socket = openSocket(str(self.OauthEntry.get()), str(self.NameEntry.get()), str(self.ChannelEntry.get()))
                self.isConnected(joinRoom(self.socket), True)
        
    def isConnected(self, boolean=None, fromConnection=False):
        if boolean != None and boolean != self.connected:
            if boolean:
                self.ConnectLabel['text']="Connected"
                self.ConnectLabel['fg']="blue"
                if fromConnection:
                    saveCredentials(self)
                    self.toggle_btn.config(relief="raised", text="Disconnect")
            else:
                if fromConnection:
                    app.ChannelLabel.delete(0, 'end')
                    app.ChannelLabel.insert('Error')
                else:
                    self.ConnectLabel['text']="Not Connected"
                    self.ConnectLabel['fg']="red"
            self.connected = boolean
        return self.connected

    def toggle(self):
        if self.toggle_btn.config('text')[-1] == 'Disconnect':
            self.toggle_btn.config(relief="raised", text="Connect")
            self.socket.close()
            self.isConnected(False)
        else:
            self.toggle_btn.config(relief="sunken", text="Disconnect")
            self.onStop()


