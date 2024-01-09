"""GUI for the settings window."""
from os import path
import customtkinter
from DictLabel import *
import GUISettings
import Settings


class GUISettingsWindow(customtkinter.CTkToplevel):
    """Settings window"""

    def __init__(self, settings: GUISettings.GUISettings, credentials: Settings.CredentialsSettings):
        super().__init__()
        self.__settings = settings
        self.__credentials = credentials
        self.__prefix = "set-"
        self.title(TXTSETTINGS)
        self.iconbitmap(path.join(path.dirname(__file__), "boticon.ico"))
        self.__settings.import_images(self.__prefix)
        self.__create_settings_top_row()
        self.__create_settings_labels()
        self.__create_settings_entries()
        self.__format_settings_window()
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def __on_closing(self):
        self.__settings.delete_images(self.__prefix)
        self.destroy()

    def __on_plus(self):
        self.__settings.change_app_font_size(True)
        self.update()

    def __on_minus(self):
        self.__settings.change_app_font_size(False)
        self.update()

    def __on_restore(self):
        self.__settings.set_font_size()
        self.update()

    def __create_settings_top_row(self):
        self.__settingstoprow = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.__fontlabel = customtkinter.CTkLabel(
            self.__settingstoprow,
            width=105,
            text="App text",
            image=self.__settings.imagedictionary["text-height"],
            compound="left",
            padx=5,
            font=self.__settings.appsize,
        )

        self.__plussettingsbutton = customtkinter.CTkButton(
            self.__settingstoprow, width=10, text="", image=self.__settings.imagedictionary["plus"], command=self.__on_plus
        )

        self.__minussettingsbutton = customtkinter.CTkButton(
            self.__settingstoprow, width=10, text="", image=self.__settings.imagedictionary["minus"], command=self.__on_minus
        )

        self.__resetsettingsbutton = customtkinter.CTkButton(
            self.__settingstoprow, width=10, text="", image=self.__settings.imagedictionary["refresh"], command=self.__on_restore
        )

        self.__fontlabel.grid(column=1, row=1, sticky="w", pady=15)
        self.__plussettingsbutton.grid(column=2, row=1)
        self.__minussettingsbutton.grid(column=3, row=1)
        self.__resetsettingsbutton.grid(column=4, row=1, sticky="w", padx=20)

    def __create_settings_labels(self):
        self.__namelabel = customtkinter.CTkLabel(self, text=TXTBOT, font=self.__settings.appsize)
        self.__oauthlabel = customtkinter.CTkLabel(self, text=TXTAUTH, font=self.__settings.appsize)
        self.__channellabel = customtkinter.CTkLabel(self, text=TXTCHANNEL, font=self.__settings.appsize)

    def __create_settings_entries(self):
        self.__nameentry = customtkinter.CTkEntry(self, width=250, font=self.__settings.appsize, textvariable=self.__credentials.namevar)

        self.__oauthentry = customtkinter.CTkEntry(
            self, width=250, show="*", font=self.__settings.appsize, textvariable=self.__credentials.oauthvar
        )

        self.__channelentry = customtkinter.CTkEntry(
            self, width=250, font=self.__settings.appsize, textvariable=self.__credentials.channelvar
        )

    def __format_settings_window(self):
        self.columnconfigure(1, weight=0)
        self.__settingstoprow.grid(column=1, columnspan=2, sticky="e")
        self.__namelabel.grid(column=1, row=2, sticky="w", padx=10, pady=5)
        self.__oauthlabel.grid(column=1, row=3, sticky="w", padx=10, pady=5)
        self.__channellabel.grid(column=1, row=4, sticky="w", padx=10, pady=5)

        self.columnconfigure(2, weight=1)
        self.__nameentry.grid(column=2, row=2, sticky="w", columnspan=2, padx=5, pady=5)
        self.__oauthentry.grid(column=2, row=3, sticky="w", columnspan=2, padx=5, pady=5)
        self.__channelentry.grid(column=2, row=4, sticky="w", columnspan=2, padx=5, pady=5)

        self.after(1, lambda: self.focus_force())
