import tkFileDialog
from DictLabel import *
from Tkinter import *
from Socket import openSocket
from Initialize import joinRoom
from Settings import *
from UserList import UserList


class Application(Frame):
    connected = False
    logNames = False
    socket = ''
    userList = UserList()
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title(txtTitle)
        self.master.geometry('350x450')
        self.create_widgets()
        loadCredentials(self)
        self.pack(side=LEFT, fill="both", expand=True)
    
    def onStart(self):
        if self.isConnected():
            self.logNames = True
            self.Start.config(relief=SKN)
            self.Stop.config(relief=RSD)
        
    def onStop(self):
        self.logNames = False
        self.Start.config(relief=RSD)
        self.Stop.config(relief=SKN)

    def addToList(self, user, message):
        self.userList.addToList(user, message, self.ListChatters, self.IgnoreEntry.get(), self.SaveEntry.get())
        if self.userList.size() == 1 and getSaveFileFromKey() != self.SaveEntry.get():
            saveFileInKey(self.SaveEntry.get())
    
    def deleteList(self):
        self.userList.deleteList(self.ListChatters)
        

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
            self.toggle_btn.config(relief=RSD, text=txtConnect)
            self.socket.close()
            self.isConnected(False)
        else:
            self.toggle_btn.config(relief=SKN, text=txtDisconnect)
        self.onStop()

    def searchFile(self):
        if self.SaveEntry.get():
            text = self.SaveEntry.get()
        else:
            text = "/"
        newLoc = tkFileDialog.asksaveasfilename(initialdir = text, title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        if newLoc:
            self.SaveEntry.delete(0, END)
            self.SaveEntry.insert(0, newLoc)
            
## actual GUI :P 
    def create_widgets(self):
        self.createLabels()
        self.createEntries()
        self.createButtons()
        self.createToggle()
        self.createList()
        self.createSave()
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
        self.ListChatters =Listbox(self, height=12, yscrollcommand=self.scrollbar.set, font=('Helvatica',12))
        self.scrollbar.config(command=self.ListChatters.yview)
        
    def createSave(self):
        self.SaveFrame =Frame(self)
        self.SaveLabel =Label(self.SaveFrame, text=txtSave)
        self.saveFileVar = IntVar()
        self.SaveCheck =Checkbutton(self.SaveFrame, variable=self.saveFileVar) 
        self.SaveEntry =Entry(self, width=35)
        self.SaveSearch=Button(self, width=1, text="...", command=self.searchFile)
        self.SaveLabel.grid(column=1, row=1)
        self.SaveCheck.grid(column=2, row=1)
        
    def setPossitions(self):
        # Column 1
        self.NameLabel.grid(column=1, row=1, sticky=W)
        self.OauthLabel.grid(column=1, row=2, sticky=W)
        self.ChannelLabel.grid(column=1, row=3, sticky=W)
        self.toggle_btn.grid(column=1, row=4)
        self.ButtonFrame.grid(column=1, row=6)
        self.IgnoreLabel.grid(column=1, row=7)
        self.SaveFrame.grid(column=1, row=8)
        
        # Column 2 
        self.NameEntry.grid(column=2, row=1, sticky=W)
        self.OauthEntry.grid(column=2, row=2, sticky=W)
        self.ChannelEntry.grid(column=2, row=3, sticky=W)
        self.ConnectLabel.grid(column=2, row=4)
        self.ListLabel.grid(column=2, row=5)

        Grid.rowconfigure(self, 6, weight=1)
        Grid.columnconfigure(self, 2, weight=1)
        
        self.ListChatters.grid(column=2, row=6, sticky=W+E+N+S)
        self.IgnoreEntry.grid(column=2, row=7, sticky=W+E)
        self.SaveEntry.grid(column=2, row=8, sticky=W+E, pady=10)

        # Column 3
        self.scrollbar.grid(column=3, row=6, sticky=N+S)
        self.SaveSearch.grid(column=3, row=8)
