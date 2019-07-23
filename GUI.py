import tkFileDialog
from DictLabel import *
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
        self.master.title(txtTitle)
        self.master.geometry('350x450')
        self.create_widgets()
        loadCredentials(self)
        #tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        self.pack()
    
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
            self.Start.config(relief=SKN)
            self.Stop.config(relief=RSD)
        
    def onStop(self):
        self.logNames = False
        self.Start.config(relief=RSD)
        self.Stop.config(relief=SKN)

    def connectSocket(self):
         if not self.isConnected() and self.toggle_btn.config(TXT)[-1] == txtDisconnect:
            if (self.OauthEntry.get() and self.NameEntry.get() and self.ChannelEntry.get()):
                self.socket = openSocket(str(self.OauthEntry.get()), str(self.NameEntry.get()), str(self.ChannelEntry.get()))
                self.isConnected(joinRoom(self.socket), True)
        
    def isConnected(self, boolean=None, fromConnection=False):
        if boolean != None and boolean != self.connected:
            if boolean:
                self.ConnectLabel[TXT]=txtConnd
                self.ConnectLabel[FG]=BL
                if fromConnection:
                    saveCredentials(self)
                    self.toggle_btn.config(relief=RSD, text=txtDisconnect)
            else:
                if fromConnection:
                    app.ChannelLabel.delete(0, END)
                    app.ChannelLabel.insert(txtERROR)
                else:
                    self.ConnectLabel[TXT]=txtNotConnd
                    self.ConnectLabel[FG]=RD
            self.connected = boolean
        return self.connected

    def toggle(self):
        if self.toggle_btn.config(TXT)[-1] == txtDisconnect:
            self.toggle_btn.config(relief=RSD, text=txtConnd)
            self.socket.close()
            self.isConnected(False)
        else:
            self.toggle_btn.config(relief=SKN, text=txtDisconnect)
        self.onStop()

    def create_widgets(self):
        self.createLabels()
        self.createEntries()
        self.createButtons()
        self.createToggle()
        self.createList()
        self.setPossitions()

    def createLabels(self):
        self.NameLabel =Label(self, text=txtBot)
        self.OauthLabel =Label(self, text=txtAuth)
        self.ChannelLabel =Label(self, text=txtChannel)
        self.ConnectLabel =Label(self, text=txtNotConnd, fg=RD)
        self.ListLabel =Label(self, text=txtListChat)
        self.IgnoreLabel =Label(self, text=txtIgnore)

    def createEntries(self):        
        self.NameEntry =Entry(self, width=35)
        self.OauthEntry =Entry(self, width=35, show="*")
        self.ChannelEntry =Entry(self, width=35)
        self.IgnoreEntry =Entry(self, width=35)

    def createButtons(self):
        self.ButtonFrame =Frame(self)
        self.Start =Button(self.ButtonFrame, width=5, text=txtStart, command=self.onStart)
        self.Stop =Button(self.ButtonFrame, width=5, text=txtStop, command=self.onStop)
        self.Clear =Button(self.ButtonFrame, width=5, text=txtClear, command=self.deleteList)
        # Location within the frame
        self.Start.grid(column=1, row=1)
        self.Stop.grid(column=1, row=2)
        self.Clear.grid(column=1, row=4)

    def createToggle(self):
        self.toggle_btn = Button(self, text=txtConnect, width=12, relief=RSD, command=self.toggle)

    def createList(self):
        self.scrollbar = Scrollbar(self)
        self.ListChatters =Listbox(self, height=15, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.ListChatters.yview)

    def setPossitions(self):
        # Column 1
        self.NameLabel.grid(column=1, row=1, sticky=W)
        self.OauthLabel.grid(column=1, row=2, sticky=W)
        self.ChannelLabel.grid(column=1, row=3, sticky=W)
        self.toggle_btn.grid(column=1, row=4)
        self.ButtonFrame.grid(column=1, row=6)
        self.IgnoreLabel.grid(column=1, row=7)
        
        # Column 2 
        self.NameEntry.grid(column=2, row=1, sticky=W)
        self.OauthEntry.grid(column=2, row=2, sticky=W)
        self.ChannelEntry.grid(column=2, row=3, sticky=W)
        self.ConnectLabel.grid(column=2, row=4)
        self.ListLabel.grid(column=2, row=5)
        self.ListChatters.grid(column=2, row=6, sticky=W+E+N+S)
        self.IgnoreEntry.grid(column=2, row=7, sticky=W+S)

        # Column 3
        self.scrollbar.grid(column=3, row=6, sticky=N+S)
