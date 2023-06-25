import customtkinter
import GUI_SettingsBase
from DictLabel import *
from PIL import Image


class GUI_SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, settings: GUI_SettingsBase.GUI_SettingsBase):
        super().__init__()
        self.settings = settings
        self.prefix = "set-"
        self.title("Settings")
        self.settings.import_images(self.prefix)
        self.create_settings_top_row(self)
        self.create_settings_labels(self)
        self.create_settings_entries(self)
        self.format_settings_window(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.settings.delete_images(self.prefix)
        self.destroy()

    def onPlus(self):
        self.settings.app_settings_font_plus()
        self.update()

    def onMinus(self):
        self.settings.app_settings_font_minus()
        self.update()

    def create_settings_top_row(self, window):
        self.SettingsTopRow = customtkinter.CTkFrame(window, fg_color=self.cget("fg_color"))

        self.FontLabel = customtkinter.CTkLabel(
            self.SettingsTopRow,
            width=105,
            text="App text",
            image=self.settings.ImageDictionary["text-height"],
            compound="left",
            padx=5,
            font=self.settings._AppSize,
        )

        self.PlusSettingsButton = customtkinter.CTkButton(
            self.SettingsTopRow,
            width=10,
            text="",
            image=self.settings.ImageDictionary["plus"],
            command=self.onPlus,
        )

        self.MinusSettingsButton = customtkinter.CTkButton(
            self.SettingsTopRow,
            width=10,
            text="",
            image=self.settings.ImageDictionary["minus"],
            command=self.onMinus,
        )

        self.FontLabel.grid(column=1, row=1, sticky="w", pady=15)
        self.PlusSettingsButton.grid(column=2, row=1)
        self.MinusSettingsButton.grid(column=3, row=1)

    def create_settings_labels(self, window):
        self.NameLabel = customtkinter.CTkLabel(window, text=txtBot, font=self.settings._AppSize)
        self.OauthLabel = customtkinter.CTkLabel(window, text=txtAuth, font=self.settings._AppSize)
        self.ChannelLabel = customtkinter.CTkLabel(window, text=txtChannel, font=self.settings._AppSize)

    def create_settings_entries(self, window):
        self.NameEntry = customtkinter.CTkEntry(window, width=250, font=self.settings._AppSize)
        self.OauthEntry = customtkinter.CTkEntry(window, width=250, show="*", font=self.settings._AppSize)
        self.ChannelEntry = customtkinter.CTkEntry(window, width=250, font=self.settings._AppSize)

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
