from os import path
import TwitchOauth
import customtkinter
import ListBoxInterface
import GUICallerInterface
import ListBox_Custom
import configparser
import os
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
        self.__ImageList: list[Image.Image] = []
        self.ImageDictionary: dict[str, customtkinter.CTkImage] = {}
        self.create_widgets()
        self.load_setting()
        self.caller = caller
        self.SettingsWindow = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        for image in self.__ImageList:
            image.close()
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
            self.DayNightButton.configure(image=self.ImageDictionary["lightbulb"])
        else:
            customtkinter.set_appearance_mode("light")
            self.DayNightButton.configure(image=self.ImageDictionary["moon"])
        self.update()

    def __change_font_size(self, font: customtkinter.CTkFont, _isUp: bool):
        if _isUp:
            font.configure(size=font["size"] + 1)
        else:
            font.configure(size=font["size"] - 1)

    def init_setup(self):
        self._AppSize = customtkinter.CTkFont(size=13)
        self._AppHighlightedSize = customtkinter.CTkFont(size=14)

    def app_settings_font_plus(self):
        self.change_app_font_size(True)

    def app_settings_font_minus(self):
        self.change_app_font_size(False)

    def change_app_font_size(self, _isUp: bool) -> None:
        self.__change_font_size(self._AppSize, _isUp)
        self.__change_font_size(self._AppHighlightedSize, _isUp)
        self.change_list_font_size(_isUp)
        self.__update_image_sizes()

        self.update()
        self.save_setting()

    def __update_image_sizes(self):
        size = self._AppSize["size"]
        for image in self.ImageDictionary:
            print(image)
            if image == "dice":
                self.ImageDictionary[image].configure(size=(size + 7, size + 7))
            # elif image == "minus" or image == "plus" or image == "text-height":
            # continue
            else:
                self.ImageDictionary[image].configure(size=(size + 2, size + 2))
            print(image)
        self.update()

    def onPlus(self) -> None:
        self.change_list_font_size(True)

    def onMinus(self) -> None:
        self.change_list_font_size(False)

    def change_list_font_size(self, _isUp: bool) -> None:
        self.__change_font_size(self._customFont, _isUp)
        self.update()
        self.save_setting()

    #############################################################
    ############ GUI configuration

    # save all gui elements into an ini file
    def save_setting(self, settings_name="settings"):
        config = configparser.ConfigParser()

        config[settings_name] = {
            "app_size": str(self._AppSize["size"]),
            "font_size": str(self._customFont["size"]),
            "reply": str(self.JoinReplyVar.get()),
        }
        with open(settings_name + ".ini", "w") as configfile:
            config.write(configfile)

    # load all gui elements from an ini file
    def load_setting(self, settings_name="settings"):
        try:
            config = configparser.ConfigParser()
            filename = settings_name + ".ini"
            if path.exists(filename):
                config.read(filename)
                if "app_size" in config[settings_name]:
                    self._AppSize.configure(size=int(config[settings_name]["app_size"]))
                    self._AppHighlightedSize.configure(size=int(config[settings_name]["app_size"]) + 1)
                    self.__update_image_sizes()
                if "font_size" in config[settings_name]:
                    self._customFont.configure(size=int(config[settings_name]["font_size"]))
                if "reply" in config[settings_name]:
                    self.JoinReplyVar.set(int(config[settings_name]["reply"]))
                self.update()

        except Exception as e:
            print("Error on reading settings.ini. Maybe save it first." + str(e))
            pass

    #############################################################
    ############ actual GUI stuff :P

    def create_widgets(self):
        self.init_setup()
        self.import_images()
        self.create_top_row_buttons()
        self.create_artifacts()
        self.create_modes_panel()
        self.create_connection_toggle()
        self.create_chatterslist()
        self.create_save_panel()
        self.create_list_modidiers()
        self.set_possitions()

    def import_images(self):
        dirname = "./img/"
        ext = ".png"
        for file in os.listdir(dirname):
            if file.endswith(ext) and not file.endswith("-dark.png"):
                file = file.removesuffix(ext)
                self.__add_image_to_dict(file)
            else:
                continue
        self.__update_image_sizes()

    def create_artifacts(self):
        self.ConnectLabel = customtkinter.CTkLabel(
            self, text=txtNotConnd, text_color=RD, width=200, font=self._AppHighlightedSize
        )
        self.ListLabel = customtkinter.CTkLabel(self, text=txtListChat, font=self._AppSize)
        self.IgnoreLabel = customtkinter.CTkLabel(self, text=txtIgnore, font=self._AppSize)
        self.IgnoreEntry = customtkinter.CTkEntry(self, width=250, font=self._AppSize)

    def on_settings_window_close(self):
        if self.SettingsWindow:
            self.SettingsWindow.destroy()
            self.SettingsWindow = None

    def create_settings_window(self):
        if self.SettingsWindow:
            return
        self.SettingsWindow = customtkinter.CTkToplevel(self)
        self.SettingsWindow.title("Settings")
        self.SettingsWindow.protocol("WM_DELETE_WINDOW", self.on_settings_window_close)
        self.create_settings_top_row(self.SettingsWindow)
        self.create_settings_labels(self.SettingsWindow)
        self.create_entries(self.SettingsWindow)
        self.format_settings_window(self.SettingsWindow)

    def __add_image_to_dict(self, name, size=(15, 15)):
        imgDark = Image.open(path.join(path.dirname(__file__), "./img/" + name + ".png"))
        self.__ImageList.append(imgDark)
        pathLight = path.join(path.dirname(__file__), "./img/" + name + "-dark.png")
        if path.exists(pathLight):
            imgLight = Image.open(pathLight)
            self.__ImageList.append(imgLight)
            self.ImageDictionary[name] = customtkinter.CTkImage(imgLight, imgDark, size=size)
        else:
            self.ImageDictionary[name] = customtkinter.CTkImage(imgDark, size=size)

    def create_settings_top_row(self, window):
        self.SettingsTopRow = customtkinter.CTkFrame(window, fg_color=self.cget("fg_color"))

        self.FontLabel = customtkinter.CTkLabel(
            self.SettingsTopRow,
            width=105,
            text="App text",
            image=self.ImageDictionary["text-height"],
            compound="left",
            padx=5,
            font=self._AppSize,
        )

        self.PlusSettingsButton = customtkinter.CTkButton(
            self.SettingsTopRow,
            width=10,
            text="",
            image=self.ImageDictionary["plus"],
            command=self.app_settings_font_plus,
        )

        self.MinusSettingsButton = customtkinter.CTkButton(
            self.SettingsTopRow,
            width=10,
            text="",
            image=self.ImageDictionary["minus"],
            command=self.app_settings_font_minus,
        )

        self.FontLabel.grid(column=1, row=1, sticky="w", pady=15)
        self.PlusSettingsButton.grid(column=2, row=1)
        self.MinusSettingsButton.grid(column=3, row=1)
        self.load_setting()

    def create_settings_labels(self, window):
        self.NameLabel = customtkinter.CTkLabel(window, text=txtBot, font=self._AppSize)
        self.OauthLabel = customtkinter.CTkLabel(window, text=txtAuth, font=self._AppSize)
        self.ChannelLabel = customtkinter.CTkLabel(window, text=txtChannel, font=self._AppSize)

    def create_entries(self, window):
        self.NameEntry = customtkinter.CTkEntry(window, width=250, font=self._AppSize)
        self.OauthEntry = customtkinter.CTkEntry(window, width=250, show="*", font=self._AppSize)
        self.ChannelEntry = customtkinter.CTkEntry(window, width=250, font=self._AppSize)

    def format_settings_window(self, window):
        window.columnconfigure(1, weight=0)
        self.SettingsTopRow.grid(column=1, columnspan=2, sticky="e")
        self.NameLabel.grid(column=1, row=2, sticky="w", padx=10, pady=5)
        self.OauthLabel.grid(column=1, row=3, sticky="w", padx=10, pady=5)
        self.ChannelLabel.grid(column=1, row=4, sticky="w", padx=10, pady=5)

        window.columnconfigure(2, weight=1)
        self.NameEntry.grid(column=2, row=2, sticky="w", columnspan=2, padx=5, pady=5)
        self.OauthEntry.grid(column=2, row=3, sticky="w", columnspan=2, padx=5, pady=5)
        self.ChannelEntry.grid(column=2, row=4, sticky="w", columnspan=2, padx=5, pady=5)

        window.after(1, lambda: window.focus_force())

    def create_top_row_buttons(self):
        self.SettingsButton = customtkinter.CTkButton(
            self, width=10, text="", image=self.ImageDictionary["gear"], command=self.create_settings_window
        )

        symbol = None

        if customtkinter.get_appearance_mode() == "light":
            symbol = self.image = self.ImageDictionary["moon"]
        else:
            symbol = self.ImageDictionary["lightbulb"]
        self.DayNightButton = customtkinter.CTkButton(self, width=10, text="", image=symbol, command=self.onDayNight)

    def create_modes_panel(self):
        self.ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.HelloMode = customtkinter.CTkLabel(self.ButtonFrame, text=txtHelloMode, font=self._AppHighlightedSize)
        self.StartHello = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.ImageDictionary["play"], text="", command=self.onStartHello
        )
        self.StopHello = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.ImageDictionary["stop"], text="", command=self.onStop
        )

        self.JoinMode = customtkinter.CTkLabel(
            self.ButtonFrame, text=txtJoinMode, padx=35, font=self._AppHighlightedSize
        )
        self.JoinReplyVar = customtkinter.IntVar()
        self.JoinReply = customtkinter.CTkSwitch(
            self.ButtonFrame,
            width=75,
            text="Reply",
            variable=self.JoinReplyVar,
            command=self.save_setting,
            font=self._AppSize,
        )
        self.StartJoin = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.ImageDictionary["play"], text="", command=self.onStartJoin
        )
        self.StopJoin = customtkinter.CTkButton(
            self.ButtonFrame, width=10, image=self.ImageDictionary["stop"], text="", command=self.onStop
        )

        self.ImageDictionary["dice"].configure(size=(20, 20))

        self.JoinPick = customtkinter.CTkButton(
            self.ButtonFrame,
            width=75,
            text=txtJoinPick,
            image=self.ImageDictionary["dice"],
            command=self.onJoinPick,
            font=self._AppSize,
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
            self, text=txtConnect, width=75, state=ON, command=self.onToggleConnection, font=self._AppSize
        )
        self.__defaultButtonColor = self.toggle_btn.cget("fg_color")

    def create_chatterslist(self):
        self._customFont = customtkinter.CTkFont(size=13)
        self.ListChatters = ListBox_Custom.ListBox_Custom(self, self._customFont)

    def create_list_modidiers(self):
        self.SizeFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.PlusButton = customtkinter.CTkButton(
            self.SizeFrame,
            width=10,
            image=self.ImageDictionary["magnifying-glass-plus"],
            text="",
            command=self.onPlus,
        )
        self.MinusButton = customtkinter.CTkButton(
            self.SizeFrame,
            width=10,
            image=self.ImageDictionary["magnifying-glass-minus"],
            text="",
            command=self.onMinus,
        )
        self.Clear = customtkinter.CTkButton(
            self.SizeFrame, width=10, image=self.ImageDictionary["trash-can"], text="", command=self.onDelete
        )

        self.SizeFrame.columnconfigure(2, weight=1)
        self.Clear.grid(column=1, row=1, sticky="w")
        self.MinusButton.grid(column=3, row=1, sticky="e")
        self.PlusButton.grid(column=4, row=1, sticky="e")

    def create_save_panel(self):
        self.SaveFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.SaveLabel = customtkinter.CTkLabel(self.SaveFrame, text=txtSave, padx=15, font=self._AppSize)
        # todo: uhmm... what?
        self.saveFileVar = customtkinter.IntVar()
        self.SaveCheck = customtkinter.CTkCheckBox(
            self.SaveFrame, variable=self.saveFileVar, text="", width=10, font=self._AppSize
        )
        self.SaveEntry = customtkinter.CTkEntry(self, font=self._AppSize)
        self.SaveSearch = customtkinter.CTkButton(
            self, width=1, text="", image=self.ImageDictionary["ellipsis"], command=self.onSearch
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
