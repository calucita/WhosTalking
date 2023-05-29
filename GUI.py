from os import path
import TwitchOauth
import customtkinter
import ListBoxInterface
import GUICallerInterface
import ListBox_Custom
from customtkinter import filedialog
from DictLabel import *
from Tools import Modes


class GUI(customtkinter.CTk, ListBoxInterface.ListBoxInterface):
    def __init__(self, caller: GUICallerInterface.GUICallerInterface):
        super().__init__()

        self.title(txtTitle)
        self.geometry("350x500")
        self.iconbitmap(path.join(path.dirname(__file__), "boticon.ico"))
        self.create_widgets()
        # self.pack(side="left", fill="both", expand=True)
        self.caller = caller

    def onStartHello(self):
        self.onStop()
        if self.caller.loggingActive(Modes.HELLO, True):
            self.StartHello.configure(state=OFF)
            self.Stop.configure(state=ON)

    def onStop(self):
        self.caller.loggingActive(Modes.NONE, True)
        self.StartHello.configure(state=ON)
        self.StartJoin.configure(state=ON)
        self.Stop.configure(state=OFF)

    def onStartJoin(self):
        self.onStop()
        if self.caller.loggingActive(Modes.POOL, True):
            self.StartJoin.configure(state=OFF)
            self.Stop.configure(state=ON)

    def onJoinPick(self):
        if self.caller.loggingActive(Modes.POOL):
            self.caller.pickUser()

    def onDelete(self):
        self.caller.deleteList()
        if self.ListChatters:
            self.ListChatters.deleteAll()

    def onToggleConnection(self):
        if self.toggle_btn.cget(TXT) == txtDisconnect:
            self.toggle_btn.configure(state=ON, fg_color=self.__defaultButtonColor, text=txtConnect)
            self.caller.setConnection(False)
        else:
            self.toggle_btn.configure(state=OFF, fg_color="gray", text=txtConnecting)
            self.update()
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
            self.ConnectLabel.configure(text=txtConnd, text_color=BL)
            if fromConnection:
                self.toggle_btn.configure(state=ON, fg_color=self.__defaultButtonColor, text=txtDisconnect)
        else:
            if fromConnection:
                # self.ChannelLabel.delete(0, END)
                if connected == 1:
                    self.ConnectLabel.configure(text=txtErrorBot, text_color=RD)
                if connected == 2:
                    self.ConnectLabel.configure(text=txtErrorChannel, text_color=RD)
                if connected == 3:
                    self.ConnectLabel.configure(text=txtErrorOauth, text_color=RD)
                if connected == 4:
                    self.ConnectLabel.configure(text=txtErrorAuthenticationFailed, text_color=RD)
                if connected == 99:
                    self.ConnectLabel.configure(text=txtError, text_color=RD)

                self.toggle_btn.configure(state=ON, fg_color=self.__defaultButtonColor, text=txtConnect)
            else:
                self.ConnectLabel.configure(text=txtNotConnd, text_color=RD)
                self.toggle_btn.configure(state=ON, fg_color=self.__defaultButtonColor, text=txtConnect)

    def isConnectActive(self):
        return self.toggle_btn.cget(TXT) == txtDisconnect

    def isFileSaveActive(self) -> bool:
        return self.saveFileVar.get() == 1

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
        self.NameLabel = customtkinter.CTkLabel(self, text=txtBot)
        self.OauthLabel = customtkinter.CTkLabel(self, text=txtAuth)
        self.ChannelLabel = customtkinter.CTkLabel(self, text=txtChannel)
        self.ConnectLabel = customtkinter.CTkLabel(self, text=txtNotConnd, text_color=RD, width=200)
        self.ConnectLabel.cget("font").configure(size=14)
        self.ListLabel = customtkinter.CTkLabel(self, text=txtListChat)
        self.IgnoreLabel = customtkinter.CTkLabel(self, text=txtIgnore)

    def create_entries(self):
        self.NameEntry = customtkinter.CTkEntry(self, width=250)
        self.OauthEntry = customtkinter.CTkEntry(self, width=250, show="*")
        self.ChannelEntry = customtkinter.CTkEntry(self, width=250)
        self.IgnoreEntry = customtkinter.CTkEntry(self, width=250)

    def create_buttons(self):
        self.ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        ## self.settingsButton = customtkinter.CTkButton(self.ButtonFrame, width=12, text=txtSettings)
        self.Clear = customtkinter.CTkButton(self.ButtonFrame, width=75, text=txtClear, command=self.onDelete)
        self.Stop = customtkinter.CTkButton(self.ButtonFrame, width=75, text=txtStop, command=self.onStop)

        self.HelloMode = customtkinter.CTkLabel(self.ButtonFrame, text=txtHelloMode)
        self.HelloMode.cget("font").configure(size=14)
        self.StartHello = customtkinter.CTkButton(self.ButtonFrame, width=75, text=txtStart, command=self.onStartHello)

        self.JoinMode = customtkinter.CTkLabel(self.ButtonFrame, text=txtJoinMode, padx=35)
        self.JoinMode.cget("font").configure(size=14)
        self.JoinReplyVar = customtkinter.IntVar()
        self.JoinReply = customtkinter.CTkCheckBox(
            self.ButtonFrame, width=75, text="Reply", variable=self.JoinReplyVar
        )
        self.StartJoin = customtkinter.CTkButton(self.ButtonFrame, width=75, text=txtStart, command=self.onStartJoin)
        self.JoinPick = customtkinter.CTkButton(self.ButtonFrame, width=75, text=txtJoinPick, command=self.onJoinPick)

        # Location within the frame
        self.Clear.grid(column=1, row=2, sticky="s")
        self.Stop.grid(column=1, row=3, sticky="s")

        self.HelloMode.grid(column=1, row=6, sticky="s")
        self.StartHello.grid(column=1, row=7, sticky="s")
        self.ButtonFrame.grid_rowconfigure(6, minsize=50)

        self.JoinMode.grid(column=1, row=9, sticky="s")
        self.JoinReply.grid(column=1, row=10, sticky="s")
        self.StartJoin.grid(column=1, row=11, sticky="s")
        self.JoinPick.grid(column=1, row=12, sticky="s")
        self.ButtonFrame.grid_rowconfigure(9, minsize=50)

    def create_toggle(self):
        self.toggle_btn = customtkinter.CTkButton(
            self, text=txtConnect, width=75, state=ON, command=self.onToggleConnection
        )
        self.__defaultButtonColor = self.toggle_btn.cget("fg_color")

    def create_list(self):
        self.ListChatters = ListBox_Custom.ListBox_Custom(self)

    def create_save(self):
        self.SaveFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.SaveLabel = customtkinter.CTkLabel(self.SaveFrame, text=txtSave, padx=15)
        # todo: uhmm... what?
        self.saveFileVar = customtkinter.IntVar()
        self.SaveCheck = customtkinter.CTkCheckBox(self.SaveFrame, variable=self.saveFileVar, text="", width=10)
        self.SaveEntry = customtkinter.CTkEntry(self, width=35)
        self.SaveSearch = customtkinter.CTkButton(self, width=1, text="...", command=self.onSearch)
        self.SaveLabel.grid(column=1, row=1)
        self.SaveCheck.grid(column=2, row=1, sticky="e")

    def set_possitions(self):
        # Column 1
        self.NameLabel.grid(column=1, row=1, sticky="w", padx=10)
        self.OauthLabel.grid(column=1, row=2, sticky="w", padx=10)
        self.ChannelLabel.grid(column=1, row=3, sticky="w", padx=10)
        self.toggle_btn.grid(column=1, row=5, pady=20)

        self.ButtonFrame.grid(column=1, row=6, sticky="n")
        self.IgnoreLabel.grid(column=1, row=7)
        self.SaveFrame.grid(column=1, row=8)

        # Column 2
        self.NameEntry.grid(column=2, row=1, sticky="w", columnspan=2, padx=5)
        self.OauthEntry.grid(column=2, row=2, sticky="w", columnspan=2, padx=5)
        self.ChannelEntry.grid(column=2, row=3, sticky="w", columnspan=2, padx=5)
        self.ConnectLabel.grid(column=2, row=5, sticky="w", pady=20)
        self.ListLabel.grid(column=2, row=6)

        self.rowconfigure(6, weight=1)
        self.columnconfigure(2, weight=1)
        if self.ListChatters:
            self.ListChatters.grid(
                column=2,
                row=6,
                columnspan=2,
                padx=5,
                sticky="w" + "e" + "n" + "s",
            )
        self.IgnoreEntry.grid(column=2, row=7, sticky="w" + "e", columnspan=2, padx=5, pady=5)
        self.SaveEntry.grid(column=2, row=8, sticky="w" + "e", pady=5)

        # Column 3
        self.SaveSearch.grid(column=3, row=8, padx=5)
