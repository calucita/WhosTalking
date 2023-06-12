from os import path
import TwitchOauth
import customtkinter
import ListBoxInterface
import GUICallerInterface
import ListBox_Custom
import configparser
from customtkinter import filedialog
from DictLabel import *
from Tools import Modes
from PIL import Image


class GUI(customtkinter.CTk, ListBoxInterface.ListBoxInterface):
    def __init__(self, caller: GUICallerInterface.GUICallerInterface):
        super().__init__()

        self.title(txtTitle)
        self.geometry("400x550")
        self.iconbitmap(path.join(path.dirname(__file__), "boticon.ico"))
        self.create_widgets()
        self.load_setting()
        # self.pack(side="left", fill="both", expand=True)
        self.caller = caller

    def onStartHello(self):
        self.onStop()
        if self.caller.loggingActive(Modes.HELLO, True):
            self.StartHello.configure(state=OFF, fg_color="gray")
            self.StopJoin.configure(state=ON, fg_color=self.__defaultButtonColor)
            self.StopHello.configure(state=ON, fg_color=self.__defaultButtonColor)
            self.update()

    def onStop(self):
        self.caller.loggingActive(Modes.NONE, True)
        self.StartHello.configure(state=ON, fg_color=self.__defaultButtonColor)
        self.StartJoin.configure(state=ON, fg_color=self.__defaultButtonColor)
        self.StopJoin.configure(state=OFF, fg_color="gray")
        self.StopHello.configure(state=OFF, fg_color="gray")
        self.update()

    def onStartJoin(self):
        self.onStop()
        if self.caller.loggingActive(Modes.POOL, True):
            self.StartJoin.configure(state=OFF, fg_color="gray")
            self.StopJoin.configure(state=ON, fg_color=self.__defaultButtonColor)
            self.StopHello.configure(state=ON, fg_color=self.__defaultButtonColor)
            self.update()

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
        return self.ConnectLabel.cget(TXT) == txtConnd

    def isFileSaveActive(self) -> bool:
        return self.saveFileVar.get() == 1

    def onDayNight(self) -> None:
        if customtkinter.get_appearance_mode() == "Light":
            customtkinter.set_appearance_mode("dark")
            self.DayNightButton.configure(image=self.DayImage)
        else:
            customtkinter.set_appearance_mode("light")
            self.DayNightButton.configure(image=self.NightImage)
        self.update()

    def onPlus(self) -> None:
        self.changeFontSize(True)

    def onMinus(self) -> None:
        self.changeFontSize(False)

    def changeFontSize(self, _isUp: bool) -> None:
        if _isUp:
            self._customFont.configure(size=self._customFont["size"] + 1)
        else:
            self._customFont.configure(size=self._customFont["size"] - 1)
        self.update()
        self.save_setting()

    #############################################################
    ############ GUI configuration

    # save all gui elements into an ini file
    def save_setting(self, settings_name="settings"):
        config = configparser.ConfigParser()

        config[settings_name] = {"font_size": str(self._customFont["size"]), "reply": str(self.JoinReplyVar.get())}
        with open(settings_name + ".ini", "w") as configfile:
            config.write(configfile)

    # load all gui elements from an ini file
    def load_setting(self, settings_name="settings"):
        try:
            config = configparser.ConfigParser()
            filename = settings_name + ".ini"
            if path.exists(filename):
                config.read(filename)

                self._customFont.configure(size=int(config[settings_name]["font_size"]))
                self.JoinReplyVar.set(int(config[settings_name]["reply"]))
                self.update()

        except Exception as e:
            print("Error on reading settings.ini. Maybe save it first." + str(e))
            pass

    #############################################################
    ############ actual GUI stuff :P

    def create_widgets(self):
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_toggle()
        self.create_list()
        self.create_save()
        self.create_list_mods()
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
        symbol = None
        self.NightImage = customtkinter.CTkImage(Image.open("./img/moon-solid.png"), size=(15, 15))
        self.DayImage = customtkinter.CTkImage(Image.open("./img/lightbulb-solid.png"), size=(15, 15))

        if customtkinter.get_appearance_mode() == "light":
            symbol = self.NightImage
        else:
            symbol = self.DayImage
        self.DayNightButton = customtkinter.CTkButton(self, width=10, text="", image=symbol, command=self.onDayNight)

        self.ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        imageStop = customtkinter.CTkImage(Image.open("./img/stop-solid.png"), size=(15, 15))
        imagePlay = customtkinter.CTkImage(Image.open("./img/play-solid.png"), size=(15, 15))
        imagePick = customtkinter.CTkImage(Image.open("./img/dice-solid.png"), size=(20, 20))

        self.HelloMode = customtkinter.CTkLabel(self.ButtonFrame, text=txtHelloMode)
        self.HelloMode.cget("font").configure(size=14)
        self.StartHello = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=imagePlay, text="", command=self.onStartHello
        )
        self.StopHello = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=imageStop, text="", command=self.onStop
        )

        self.JoinMode = customtkinter.CTkLabel(self.ButtonFrame, text=txtJoinMode, padx=35)
        self.JoinMode.cget("font").configure(size=14)
        self.JoinReplyVar = customtkinter.IntVar()
        self.JoinReply = customtkinter.CTkSwitch(
            self.ButtonFrame, width=75, text="Reply", variable=self.JoinReplyVar, command=self.save_setting
        )
        self.StartJoin = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=imagePlay, text="", command=self.onStartJoin
        )
        self.StopJoin = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=imageStop, text="", command=self.onStop
        )
        self.JoinPick = customtkinter.CTkButton(
            self.ButtonFrame, width=75, text=txtJoinPick, image=imagePick, command=self.onJoinPick
        )

        # Location within the frame

        self.HelloMode.grid(column=1, row=6, columnspan=2, sticky="s")
        self.StartHello.grid(column=1, row=7, padx=5, sticky="e")
        self.StopHello.grid(column=2, row=7, padx=5, sticky="w")
        self.ButtonFrame.grid_rowconfigure(6, minsize=50)

        self.JoinMode.grid(column=1, row=9, columnspan=2, sticky="s")
        self.JoinReply.grid(column=1, row=10, columnspan=2, sticky="s")
        self.StartJoin.grid(column=1, row=11, padx=5, sticky="e")
        self.StopJoin.grid(column=2, row=11, padx=5, sticky="w")
        self.JoinPick.grid(column=1, row=12, columnspan=2, pady=5, sticky="s")
        self.ButtonFrame.grid_rowconfigure(9, minsize=70)

    def create_toggle(self):
        self.toggle_btn = customtkinter.CTkButton(
            self, text=txtConnect, width=75, state=ON, command=self.onToggleConnection
        )
        self.__defaultButtonColor = self.toggle_btn.cget("fg_color")

    def create_list(self):
        self._customFont = customtkinter.CTkFont(size=13)
        self.ListChatters = ListBox_Custom.ListBox_Custom(self, self._customFont)

    def create_list_mods(self):
        self.SizeFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        imagePlus = customtkinter.CTkImage(Image.open("./img/magnifying-glass-plus-solid.png"), size=(15, 15))
        imageMinus = customtkinter.CTkImage(Image.open("./img/magnifying-glass-minus-solid.png"), size=(15, 15))
        imageTrash = customtkinter.CTkImage(Image.open("./img/trash-can-solid.png"), size=(15, 15))

        self.PlusButton = customtkinter.CTkButton(
            self.SizeFrame, width=10, image=imagePlus, text="", command=self.onPlus
        )
        self.MinusButton = customtkinter.CTkButton(
            self.SizeFrame, width=10, image=imageMinus, text="", command=self.onMinus
        )
        self.Clear = customtkinter.CTkButton(
            self.SizeFrame, width=10, image=imageTrash, text="", command=self.onDelete
        )

        self.SizeFrame.columnconfigure(2, weight=1)
        self.Clear.grid(column=1, row=1, sticky="w")
        self.MinusButton.grid(column=3, row=1, sticky="e")
        self.PlusButton.grid(column=4, row=1, sticky="e")

    def create_save(self):
        imageDots = customtkinter.CTkImage(Image.open("./img/ellipsis-solid.png"), size=(15, 15))

        self.SaveFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.SaveLabel = customtkinter.CTkLabel(self.SaveFrame, text=txtSave, padx=15)
        # todo: uhmm... what?
        self.saveFileVar = customtkinter.IntVar()
        self.SaveCheck = customtkinter.CTkCheckBox(self.SaveFrame, variable=self.saveFileVar, text="", width=10)
        self.SaveEntry = customtkinter.CTkEntry(self)
        self.SaveSearch = customtkinter.CTkButton(self, width=1, text="", image=imageDots, command=self.onSearch)
        self.SaveLabel.grid(column=1, row=1)
        self.SaveCheck.grid(column=2, row=1, sticky="e")

    def set_possitions(self):
        # Column 1
        self.columnconfigure(1, weight=0)
        self.NameLabel.grid(column=1, row=2, sticky="w", padx=10)
        self.OauthLabel.grid(column=1, row=3, sticky="w", padx=10)
        self.ChannelLabel.grid(column=1, row=4, sticky="w", padx=10)
        self.toggle_btn.grid(column=1, row=6, pady=20)

        self.ButtonFrame.grid(column=1, row=7, sticky="n")
        self.IgnoreLabel.grid(column=1, row=9)
        self.SaveFrame.grid(column=1, row=10)

        # Column 2
        self.columnconfigure(2, weight=1)
        self.NameEntry.grid(column=2, row=2, sticky="w", columnspan=2, padx=5)
        self.OauthEntry.grid(column=2, row=3, sticky="w", columnspan=2, padx=5)
        self.ChannelEntry.grid(column=2, row=4, sticky="w", columnspan=2, padx=5)
        self.ConnectLabel.grid(column=2, row=6, sticky="w", pady=20)
        self.ListLabel.grid(column=2, row=7)

        self.rowconfigure(7, weight=1)
        if self.ListChatters:
            self.ListChatters.grid(
                column=2,
                row=7,
                columnspan=2,
                padx=5,
                sticky="w" + "e" + "n" + "s",
            )
        self.SizeFrame.grid(column=2, row=8, sticky="w" + "e", columnspan=2, padx=5)
        self.IgnoreEntry.grid(column=2, row=9, sticky="w" + "e", columnspan=2, padx=5, pady=5)
        self.SaveEntry.grid(column=2, row=10, sticky="w" + "e", pady=5)

        # Column 3
        self.columnconfigure(3, weight=0)
        self.DayNightButton.grid(column=3, row=1, padx=5, pady=5, sticky="e")
        self.SaveSearch.grid(column=3, row=10, padx=5, sticky="e")
