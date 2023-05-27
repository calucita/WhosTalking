from os import path
import TwitchOauth
import tkinter
import ListBoxInterface
import GUICallerInterface
from tkinter import filedialog
from DictLabel import *
from Tools import Modes


class GUI(tkinter.Frame, ListBoxInterface.ListBoxInterface):
    def __init__(self, caller: GUICallerInterface.GUICallerInterface, master=None):
        tkinter.Frame.__init__(self, master)
        if not master:
            raise Exception("something went worng with the GUI")
        self.master = master
        self.master.title(txtTitle)
        self.master.geometry("350x450")
        self.master.iconbitmap(path.join(path.dirname(__file__), "boticon.ico"))
        self.create_widgets()
        self.pack(side=tkinter.LEFT, fill="both", expand=True)
        self.caller = caller

    def onStartHello(self):
        self.onStop()
        if self.caller.loggingActive(Modes.HELLO, True):
            self.StartHello.config(relief=SKN)
            self.Stop.config(relief=RSD)

    def onStop(self):
        self.caller.loggingActive(Modes.NONE, True)
        self.StartHello.config(relief=RSD)
        self.StartJoin.config(relief=RSD)
        self.Stop.config(relief=SKN)

    def onStartJoin(self):
        self.onStop()
        if self.caller.loggingActive(Modes.POOL, True):
            self.StartJoin.config(relief=SKN)
            self.Stop.config(relief=RSD)

    def onJoinPick(self):
        if self.caller.loggingActive(Modes.POOL):
            self.caller.pickUser()

    def onDelete(self):
        self.caller.deleteList()
        if self.ListChatters:
            self.ListChatters.delete(0, END)

    def onToggleConnection(self):
        if self.toggle_btn.config(TXT)[-1] == txtDisconnect:
            self.toggle_btn.config(relief=RSD, text=txtConnect)
            self.caller.setConnection(False)
        else:
            self.toggle_btn.config(relief=SKN, text=txtDisconnect)
            self.caller.setConnection(True)
        self.onStop()

    def onSearch(self):
        if self.SaveEntry.get():
            text = self.SaveEntry.get()
        else:
            text = "/"
        newLoc = filedialog.asksaveasfilename(
            initialdir=text,
            title="Select file",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
        )
        if newLoc:
            self.SaveEntry.delete(0, END)
            self.SaveEntry.insert(0, newLoc)

    def getOauthStr(self):
        # print(self.OauthEntry.get())
        if self.OauthEntry.get() == "":
            oauth = TwitchOauth.TwitchOauth()
            val = oauth.authenticate()
            if not val or val == "  ":
                self.setConnectButton(False, 0, False)
                return ""
            self.OauthEntry.insert(0, "oauth:" + val)
        return self.OauthEntry.get()

    def getNameStr(self):
        return self.NameEntry.get()

    def getChnlStr(self) -> str:
        return self.ChannelEntry.get()

    def getIngoreStr(self) -> str:
        return self.IgnoreEntry.get()

    def getSaveStr(self) -> str:
        return self.SaveEntry.get()

    def setConnectButton(self, boolean=False, connected=0, fromConnection=False):
        if boolean:
            self.ConnectLabel[TXT] = txtConnd
            self.ConnectLabel[FG] = BL
            if fromConnection:
                self.toggle_btn.config(relief=RSD, text=txtDisconnect)
        else:
            if fromConnection:
                # self.ChannelLabel.delete(0, END)
                if connected == 1:
                    self.ConnectLabel[TXT] = txtErrorBot
                if connected == 2:
                    self.ConnectLabel[TXT] = txtErrorChannel
                if connected == 3:
                    self.ConnectLabel[TXT] = txtErrorOauth
                if connected == 4:
                    self.ConnectLabel[TXT] = txtErrorAuthenticationFailed
                if connected == 99:
                    self.ConnectLabel[TXT] = txtError

                self.toggle_btn.config(relief=RSD, text=txtConnect)
            else:
                self.ConnectLabel[TXT] = txtNotConnd
                self.ConnectLabel[FG] = RD
                self.toggle_btn.config(relief=RSD, text=txtConnect)

    def isConnectActive(self):
        return self.toggle_btn.config(TXT)[-1] == txtDisconnect

    #############################################################
    ############ actual GUI stuff :P

    def create_widgets(self):
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_toggle()
        self.create_list()
        self.create_save()
        self.set_possitions()

    def create_labels(self):
        self.NameLabel = tkinter.Label(self, text=txtBot)
        self.OauthLabel = tkinter.Label(self, text=txtAuth)
        self.ChannelLabel = tkinter.Label(self, text=txtChannel)
        self.ConnectLabel = tkinter.Label(self, text=txtNotConnd, fg=RD)
        self.ListLabel = tkinter.Label(self, text=txtListChat)
        self.IgnoreLabel = tkinter.Label(self, text=txtIgnore)

    def create_entries(self):
        self.NameEntry = tkinter.Entry(self, width=35)
        self.OauthEntry = tkinter.Entry(self, width=35, show="*")
        self.ChannelEntry = tkinter.Entry(self, width=35)
        self.IgnoreEntry = tkinter.Entry(self, width=35)

    def create_buttons(self):
        self.ButtonFrame = tkinter.Frame(self, height=40)
        ## self.settingsButton = tkinter.Button(self.ButtonFrame, width=12, text=txtSettings)
        self.Clear = tkinter.Button(self.ButtonFrame, width=5, text=txtClear, command=self.onDelete)
        self.Stop = tkinter.Button(self.ButtonFrame, width=5, text=txtStop, command=self.onStop)

        self.HelloMode = tkinter.Label(self.ButtonFrame, text=txtHelloMode)
        self.StartHello = tkinter.Button(self.ButtonFrame, width=5, text=txtStart, command=self.onStartHello)

        self.JoinMode = tkinter.Label(self.ButtonFrame, text=txtJoinMode)
        self.StartJoin = tkinter.Button(self.ButtonFrame, width=5, text=txtStart, command=self.onStartJoin)
        self.JoinPick = tkinter.Button(self.ButtonFrame, width=5, text=txtJoinPick, command=self.onJoinPick)

        # Location within the frame
        ## self.settingsButton.grid(column=1, row=1, sticky=N, pady=(0,50))
        self.Clear.grid(column=1, row=2, sticky=tkinter.S)
        self.Stop.grid(column=1, row=3, sticky=tkinter.S)

        self.HelloMode.grid(column=1, row=6, sticky=tkinter.S)
        self.StartHello.grid(column=1, row=7, sticky=tkinter.S)
        self.ButtonFrame.grid_rowconfigure(6, minsize=40)

        self.JoinMode.grid(column=1, row=9, sticky=tkinter.S)
        self.StartJoin.grid(column=1, row=10, sticky=tkinter.S)
        self.JoinPick.grid(column=1, row=11, sticky=tkinter.S)
        self.ButtonFrame.grid_rowconfigure(9, minsize=40)

    def create_toggle(self):
        self.toggle_btn = tkinter.Button(self, text=txtConnect, width=12, relief=RSD, command=self.onToggleConnection)

    def create_list(self):
        self.scrollbar = tkinter.Scrollbar(self)
        self.ListChatters = tkinter.Listbox(self, height=12, yscrollcommand=self.scrollbar.set, font=("Helvatica", 12))
        self.scrollbar.config(command=self.ListChatters.yview)

    def create_save(self):
        self.SaveFrame = tkinter.Frame(self)
        self.SaveLabel = tkinter.Label(self.SaveFrame, text=txtSave)
        self.saveFileVar = tkinter.IntVar()
        self.SaveCheck = tkinter.Checkbutton(self.SaveFrame, variable=self.saveFileVar)
        self.SaveEntry = tkinter.Entry(self, width=35)
        self.SaveSearch = tkinter.Button(self, width=1, text="...", command=self.onSearch)
        self.SaveLabel.grid(column=1, row=1)
        self.SaveCheck.grid(column=2, row=1)

    def set_possitions(self):
        # Column 1
        self.NameLabel.grid(column=1, row=1, sticky=tkinter.W, padx=15)
        self.OauthLabel.grid(column=1, row=2, sticky=tkinter.W, padx=15)
        self.ChannelLabel.grid(column=1, row=3, sticky=tkinter.W, padx=15)
        self.toggle_btn.grid(column=1, row=5)

        self.ButtonFrame.grid(column=1, row=6, sticky=tkinter.N, pady=30)
        self.IgnoreLabel.grid(column=1, row=7)
        self.SaveFrame.grid(column=1, row=8)

        # Column 2
        self.NameEntry.grid(column=2, row=1, sticky=tkinter.W)
        self.OauthEntry.grid(column=2, row=2, sticky=tkinter.W)
        self.ChannelEntry.grid(column=2, row=3, sticky=tkinter.W)
        self.ConnectLabel.grid(column=2, row=5)
        self.ListLabel.grid(column=2, row=6)

        self.rowconfigure(6, weight=1)
        self.columnconfigure(2, weight=1)
        if self.ListChatters:
            self.ListChatters.grid(column=2, row=6, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)
        self.IgnoreEntry.grid(column=2, row=7, sticky=tkinter.W + tkinter.E)
        self.SaveEntry.grid(column=2, row=8, sticky=tkinter.W + tkinter.E, pady=10)

        # Column 3
        self.scrollbar.grid(column=3, row=6, sticky=tkinter.N + tkinter.S)
        self.SaveSearch.grid(column=3, row=8)
