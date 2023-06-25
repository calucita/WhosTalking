from os import path
import TwitchOauth
import customtkinter
import ListBoxInterface
import GUICallerInterface
import ListBox_Custom
import GUI_SettingsBase
import GUI_SettingsWindow
from customtkinter import filedialog
from DictLabel import *
from Tools import Modes


class GUI(customtkinter.CTk, ListBoxInterface.ListBoxInterface):
    def __init__(self, caller: GUICallerInterface.GUICallerInterface):
        super().__init__()
        self.title(txtTitle)
        self.geometry("400x550")
        self.iconbitmap(path.join(path.dirname(__file__), "boticon.ico"))
        self.caller = caller
        self.SettingsWindow = None
        self.prefix = "main-"
        self.settings = GUI_SettingsBase.GUI_SettingsBase()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.settings.delete_images(self.prefix)
        self.destroy()

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
        """if self.OauthEntry.get() == "":
        oauth = TwitchOauth.TwitchOauth()
        val = oauth.authenticate()
        if not val or val == "  ":
            self.setConnectButton(False, 0, False)
            return "" """
        # self.OauthEntry.insert(0, "oauth:" + val)
        return ""  # self.OauthEntry.get()

    def getNameStr(self):
        return ""  # self.NameEntry.get()

    def getChnlStr(self) -> str:
        return ""  # self.ChannelEntry.get()

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
            self.DayNightButton.configure(image=self.settings.ImageDictionary["lightbulb"])
        else:
            customtkinter.set_appearance_mode("light")
            self.DayNightButton.configure(image=self.settings.ImageDictionary["moon"])
        self.update()

    def onPlus(self) -> None:
        self.settings.change_list_font_size(True)
        self.update()

    def onMinus(self) -> None:
        self.settings.change_list_font_size(False)
        self.update()

    def create_settings_window(self):
        GUI_SettingsWindow.GUI_SettingsWindow(self.settings)

    #############################################################
    ############ actual GUI stuff :P

    def create_widgets(self):
        self.settings.import_images(self.prefix)
        self.create_top_row_buttons()
        self.create_artifacts()
        self.create_modes_panel()
        self.create_connection_toggle()
        self.create_chatterslist()
        self.create_save_panel()
        self.create_list_modidiers()
        self.set_possitions()

    def create_artifacts(self):
        self.ConnectLabel = customtkinter.CTkLabel(
            self, text=txtNotConnd, text_color=RD, width=200, font=self.settings._AppHighlightedSize
        )
        self.ListLabel = customtkinter.CTkLabel(self, text=txtListChat, font=self.settings._AppSize)
        self.IgnoreLabel = customtkinter.CTkLabel(self, text=txtIgnore, font=self.settings._AppSize)
        self.IgnoreEntry = customtkinter.CTkEntry(self, width=250, font=self.settings._AppSize)

    def create_top_row_buttons(self):
        self.SettingsButton = customtkinter.CTkButton(
            self, width=10, text="", image=self.settings.ImageDictionary["gear"], command=self.create_settings_window
        )

        symbol = None

        if customtkinter.get_appearance_mode() == "light":
            symbol = self.image = self.settings.ImageDictionary["moon"]
        else:
            symbol = self.settings.ImageDictionary["lightbulb"]
        self.DayNightButton = customtkinter.CTkButton(self, width=10, text="", image=symbol, command=self.onDayNight)

    def create_modes_panel(self):
        self.ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.HelloMode = customtkinter.CTkLabel(
            self.ButtonFrame, text=txtHelloMode, font=self.settings._AppHighlightedSize
        )
        self.StartHello = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.settings.ImageDictionary["play"], text="", command=self.onStartHello
        )
        self.StopHello = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.settings.ImageDictionary["stop"], text="", command=self.onStop
        )

        self.JoinMode = customtkinter.CTkLabel(
            self.ButtonFrame, text=txtJoinMode, padx=35, font=self.settings._AppHighlightedSize
        )
        self.JoinReply = customtkinter.CTkSwitch(
            self.ButtonFrame,
            width=75,
            text="Reply",
            variable=self.settings.JoinReplyVar,
            command=self.settings.save_setting,
            font=self.settings._AppSize,
        )
        self.StartJoin = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.settings.ImageDictionary["play"], text="", command=self.onStartJoin
        )
        self.StopJoin = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.settings.ImageDictionary["stop"], text="", command=self.onStop
        )

        self.settings.ImageDictionary["dice"].configure(size=(20, 20))

        self.JoinPick = customtkinter.CTkButton(
            self.ButtonFrame,
            width=75,
            text=txtJoinPick,
            image=self.settings.ImageDictionary["dice"],
            command=self.onJoinPick,
            font=self.settings._AppSize,
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

    def create_connection_toggle(self):
        self.toggle_btn = customtkinter.CTkButton(
            self, text=txtConnect, width=75, state=ON, command=self.onToggleConnection, font=self.settings._AppSize
        )
        self.__defaultButtonColor = self.toggle_btn.cget("fg_color")

    def create_chatterslist(self):
        self.ListChatters = ListBox_Custom.ListBox_Custom(self, self.settings._customFont)

    def create_list_modidiers(self):
        self.SizeFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.PlusButton = customtkinter.CTkButton(
            self.SizeFrame,
            width=10,
            image=self.settings.ImageDictionary["lupa-plus"],
            text="",
            command=self.onPlus,
        )
        self.MinusButton = customtkinter.CTkButton(
            self.SizeFrame,
            width=10,
            image=self.settings.ImageDictionary["lupa-minus"],
            text="",
            command=self.onMinus,
        )
        self.Clear = customtkinter.CTkButton(
            self.SizeFrame, width=10, image=self.settings.ImageDictionary["trash-can"], text="", command=self.onDelete
        )

        self.SizeFrame.columnconfigure(2, weight=1)
        self.Clear.grid(column=1, row=1, sticky="w")
        self.MinusButton.grid(column=3, row=1, sticky="e")
        self.PlusButton.grid(column=4, row=1, sticky="e")

    def create_save_panel(self):
        self.SaveFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.SaveLabel = customtkinter.CTkLabel(self.SaveFrame, text=txtSave, padx=15, font=self.settings._AppSize)
        # todo: uhmm... what?
        self.saveFileVar = customtkinter.IntVar()
        self.SaveCheck = customtkinter.CTkCheckBox(
            self.SaveFrame, variable=self.saveFileVar, text="", width=10, font=self.settings._AppSize
        )
        self.SaveEntry = customtkinter.CTkEntry(self, font=self.settings._AppSize)
        self.SaveSearch = customtkinter.CTkButton(
            self, width=1, text="", image=self.settings.ImageDictionary["ellipsis"], command=self.onSearch
        )
        self.SaveLabel.grid(column=1, row=1)
        self.SaveCheck.grid(column=2, row=1, sticky="e")

    def set_possitions(self):
        # Column 1
        self.columnconfigure(1, weight=0)
        self.SettingsButton.grid(column=1, row=1, padx=5, pady=5, sticky="w")
        self.toggle_btn.grid(column=1, row=6, pady=20)

        self.ButtonFrame.grid(column=1, row=7, sticky="n")
        self.IgnoreLabel.grid(column=1, row=9)
        self.SaveFrame.grid(column=1, row=10)

        # Column 2
        self.columnconfigure(2, weight=1)
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
