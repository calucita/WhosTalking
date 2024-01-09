"""Main GUI implementation"""
from os import path
import customtkinter
from customtkinter import filedialog
from Tools import Modes
from DictLabel import *
import GUICallerInterface
import CustomListBox
import GUISettings
import GUISettingsWindow
import ListBoxInterface
import Settings


class GUI(customtkinter.CTk, ListBoxInterface.ListBoxInterface):
    """Main window GUI."""

    def __init__(self, caller: GUICallerInterface.GUICallerInterface):
        super().__init__()
        self.__defaulticoncolor = GR
        self.__caller = caller
        self.__prefix = "main-"
        self.__settings = GUISettings.GUISettings()
        self.__credentials = Settings.CredentialsSettings()
        self.title(TXTTITLE)
        self.geometry("400x550")
        self.iconbitmap(path.join(path.dirname(__file__), "boticon.ico"))
        self.__create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def get_credentials(self) -> Settings.CredentialsSettings:
        """Get the credentials handler instance

        Returns:
            Settings.CredentialsSettings
        """
        return self.__credentials

    def get_chnl_str(self) -> str:
        return self.__credentials.channelvar.get()

    def get_save_str(self) -> str:
        return self.__saveentry.get()

    def get_ingore_str(self) -> str:
        return self.__ignoreentry.get()

    def is_reply_active(self) -> bool:
        """Retrieves the state of the reply toggle

        Returns:
            bool: True, is reply active; otherwise, False.
        """
        return self.__settings.joinreplyvar.get() == 1

    def __on_closing(self) -> None:
        self.__settings.delete_images(self.__prefix)
        self.destroy()

    def __on_start_hello(self) -> None:
        self.__on_stop()
        if self.__caller.logging_active(Modes.HELLO, True):
            self.__starthello.configure(state=OFF, fg_color=self.__defaulticoncolor)
            self.__stopjoin.configure(state=ON, fg_color=self.__defaultbuttoncolor)
            self.__stophello.configure(state=ON, fg_color=self.__defaultbuttoncolor)
            self.update()

    def __on_stop(self) -> None:
        self.__caller.logging_active(Modes.NONE, True)
        self.__starthello.configure(state=ON, fg_color=self.__defaultbuttoncolor)
        self.__startjoin.configure(state=ON, fg_color=self.__defaultbuttoncolor)
        self.__stopjoin.configure(state=OFF, fg_color=self.__defaulticoncolor)
        self.__stophello.configure(state=OFF, fg_color=self.__defaulticoncolor)
        self.update()

    def __on_start_join(self) -> None:
        self.__on_stop()
        if self.__caller.logging_active(Modes.POOL, True):
            self.__startjoin.configure(state=OFF, fg_color=self.__defaulticoncolor)
            self.__stopjoin.configure(state=ON, fg_color=self.__defaultbuttoncolor)
            self.__stophello.configure(state=ON, fg_color=self.__defaultbuttoncolor)
            self.update()

    def __on_join_pick(self) -> None:
        if self.__caller.logging_active(Modes.POOL):
            self.__caller.pick_user()

    def __on_delete(self) -> None:
        self.__caller.delete_list()
        if self._listchatters:
            self._listchatters.delete_all()

    def __on_toggle_connection(self) -> None:
        if self.toggle_btn.cget(TXT) == TXTDISCONNECT:
            self.toggle_btn.configure(state=ON, fg_color=self.__defaultbuttoncolor, text=TXTCONNECT)
            self.__caller.set_connection(False)
        else:
            self.toggle_btn.configure(state=OFF, fg_color=self.__defaulticoncolor, text=TXTCONNECTING)
            self.update()
            if not self.__credentials.namevar.get() or not self.__credentials.channelvar.get():
                self.toggle_btn.configure(state=ON, fg_color=self.__defaultbuttoncolor, text=TXTCONNECT)
                self.__connectlabel.configure(text=TXTERRORNODATA, text_color=RD)
                self.__create_settings_window()
            else:
                self.__caller.set_connection(True)
        self.__on_stop()

    def __on_search(self) -> None:
        if self.__saveentry.get():
            text = self.__saveentry.get()
        else:
            text = "/"
        newloc = filedialog.asksaveasfilename(
            initialdir=text,
            title="Select file",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
        )
        if newloc:
            self.__saveentry.delete(0, END)
            self.__saveentry.insert(0, newloc)

    def set_connect_button(self, status=False, errorcode=0, fromconnection=False) -> None:
        """Updates the state of the connect GUI feedback.

        Args:
            status (bool, optional): State of the connection. Defaults to False.
            errorcode (int, optional): Error code. Defaults to 0.
            fromconnection (bool, optional): where the update originates. Defaults to False.
        """
        if status:
            self.__connectlabel.configure(text=TXTCONNECTED, text_color=BL)
            if fromconnection:
                self.toggle_btn.configure(state=ON, fg_color=self.__defaultbuttoncolor, text=TXTDISCONNECT)
        else:
            if fromconnection:
                # self.ChannelLabel.delete(0, END)
                if errorcode == 1:
                    self.__connectlabel.configure(text=TXTERRORBOT, text_color=RD)
                if errorcode == 2:
                    self.__connectlabel.configure(text=TXTERRORCHANNEL, text_color=RD)
                if errorcode == 3:
                    self.__connectlabel.configure(text=TXTERROROAUTH, text_color=RD)
                if errorcode == 4:
                    self.__connectlabel.configure(text=TXTERRORAUTHFAIL, text_color=RD)
                if errorcode == 99:
                    self.__connectlabel.configure(text=TXTERROR, text_color=RD)

                self.toggle_btn.configure(state=ON, fg_color=self.__defaultbuttoncolor, text=TXTCONNECT)
            else:
                self.__connectlabel.configure(text=TXTNOTCONNECTED, text_color=RD)
                self.toggle_btn.configure(state=ON, fg_color=self.__defaultbuttoncolor, text=TXTCONNECT)

    def is_connection_active(self) -> bool:
        """Retrieves the connection status as displayed in the GUI.

        Returns:
            bool: True, if active; otherwise, False.
        """
        return self.__connectlabel.cget(TXT) == TXTCONNECTED

    def is_file_save_active(self) -> bool:
        """Retrieves the selection for the save to file feature.

        Returns:
            bool: True if active; otherwise, False.
        """
        return self.__savefilevar.get() == 1

    def __set_theme(self, mode: str = "") -> None:
        if mode != "dark" and mode != "light":
            if customtkinter.get_appearance_mode() == "Light":
                mode = "dark"
            else:
                mode = "light"

        if mode == "light":
            customtkinter.set_appearance_mode("light")
            self._daynightbutton.configure(image=self.__settings.imagedictionary["moon"])
        else:
            customtkinter.set_appearance_mode("dark")
            self._daynightbutton.configure(image=self.__settings.imagedictionary["lightbulb"])

        self.update()
        self.__settings.save_settings()

    def __on_plus(self) -> None:
        self.__settings.change_list_font_size(True)
        self.update()

    def __on_minus(self) -> None:
        self.__settings.change_list_font_size(False)
        self.update()

    def __create_settings_window(self):
        GUISettingsWindow.GUISettingsWindow(self.__settings, self.__credentials)

    #############################################################
    ############ actual GUI stuff :P

    def __create_widgets(self):
        self.__settings.import_images(self.__prefix)
        self.__create_connection_toggle()
        self.__create_top_row_buttons()
        self.__create_artifacts()
        self.__create_modes_panel()
        self.__create_chatterslist()
        self.__create_save_panel()
        self.__create_list_modidiers()
        self.__set_possitions()

    def __create_artifacts(self):
        self.__connectlabel = customtkinter.CTkLabel(
            self, text=TXTNOTCONNECTED, text_color=RD, width=200, font=self.__settings.apphighlightedsize
        )
        self.__listlabel = customtkinter.CTkLabel(self, text=TXTLISTCHAT, font=self.__settings.appsize)
        self.__ignorelabel = customtkinter.CTkLabel(self, text=TXTIGNORE, font=self.__settings.appsize)
        self.__ignoreentry = customtkinter.CTkEntry(self, width=250, font=self.__settings.appsize)

    def __create_top_row_buttons(self):
        self.__settingsbutton = customtkinter.CTkButton(
            self, width=10, text="", image=self.__settings.imagedictionary["gear"], command=self.__create_settings_window
        )

        symbol = self.__settings.imagedictionary["lightbulb"]

        self._daynightbutton = customtkinter.CTkButton(self, width=10, text="", image=symbol, command=self.__set_theme)
        self.__set_theme(self.__settings.themevar.get())

    def __create_modes_panel(self):
        self.__buttonframe = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.__hellomode = customtkinter.CTkLabel(self.__buttonframe, text=TXTHELLOMODE, font=self.__settings.apphighlightedsize)
        self.__starthello = customtkinter.CTkButton(
            self.__buttonframe, width=10, image=self.__settings.imagedictionary["play"], text="", command=self.__on_start_hello
        )
        self.__stophello = customtkinter.CTkButton(
            self.__buttonframe, width=10, image=self.__settings.imagedictionary["stop"], text="", command=self.__on_stop
        )

        self.__joinmode = customtkinter.CTkLabel(self.__buttonframe, text=TXTJOINMODE, padx=35, font=self.__settings.apphighlightedsize)
        self.__joinreply = customtkinter.CTkSwitch(
            self.__buttonframe,
            width=75,
            text="Reply",
            variable=self.__settings.joinreplyvar,
            command=self.__settings.save_settings,
            font=self.__settings.appsize,
        )
        self.__startjoin = customtkinter.CTkButton(
            self.__buttonframe, width=10, image=self.__settings.imagedictionary["play"], text="", command=self.__on_start_join
        )
        self.__stopjoin = customtkinter.CTkButton(
            self.__buttonframe, width=10, image=self.__settings.imagedictionary["stop"], text="", command=self.__on_stop
        )

        self.__joinpick = customtkinter.CTkButton(
            self.__buttonframe,
            width=75,
            text=TXTJOINPICK,
            image=self.__settings.imagedictionary["dice"],
            command=self.__on_join_pick,
            font=self.__settings.appsize,
        )

        # Location within the frame

        self.__hellomode.grid(column=1, row=6, columnspan=2, sticky="s")
        self.__starthello.grid(column=1, row=7, padx=5, sticky="e")
        self.__stophello.grid(column=2, row=7, padx=5, sticky="w")
        self.__buttonframe.grid_rowconfigure(6, minsize=50)

        self.__joinmode.grid(column=1, row=9, columnspan=2, sticky="s")
        self.__joinreply.grid(column=1, row=10, columnspan=2, sticky="s")
        self.__startjoin.grid(column=1, row=11, padx=5, sticky="e")
        self.__stopjoin.grid(column=2, row=11, padx=5, sticky="w")
        self.__joinpick.grid(column=1, row=12, columnspan=2, pady=5, sticky="s")
        self.__buttonframe.grid_rowconfigure(9, minsize=70)

    def __create_connection_toggle(self):
        self.toggle_btn = customtkinter.CTkButton(
            self,
            text=TXTCONNECT,
            width=75,
            state=ON,
            command=self.__on_toggle_connection,
            font=self.__settings.appsize,
        )
        self.__defaultbuttoncolor = self.toggle_btn.cget("fg_color")

    def __create_chatterslist(self):
        self._listchatters = CustomListBox.CustomListBox(self, self.__settings.customfont)

    def __create_list_modidiers(self):
        self.__sizeframe = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.__plusbutton = customtkinter.CTkButton(
            self.__sizeframe, width=10, image=self.__settings.imagedictionary["lupa-plus"], text="", command=self.__on_plus
        )
        self.__minusbutton = customtkinter.CTkButton(
            self.__sizeframe, width=10, image=self.__settings.imagedictionary["lupa-minus"], text="", command=self.__on_minus
        )
        self.__clear = customtkinter.CTkButton(
            self.__sizeframe, width=10, image=self.__settings.imagedictionary["trash-can"], text="", command=self.__on_delete
        )

        self.__sizeframe.columnconfigure(2, weight=1)
        self.__clear.grid(column=1, row=1, sticky="w")
        self.__minusbutton.grid(column=3, row=1, sticky="e")
        self.__plusbutton.grid(column=4, row=1, sticky="e")

    def __create_save_panel(self):
        self.__saveframe = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.__savelabel = customtkinter.CTkLabel(self.__saveframe, text=TXTSAVE, padx=15, font=self.__settings.appsize)

        self.__savefilevar = customtkinter.IntVar()
        self.__savecheck = customtkinter.CTkCheckBox(
            self.__saveframe, variable=self.__savefilevar, text="", width=10, font=self.__settings.appsize
        )
        self.__saveentry = customtkinter.CTkEntry(self, font=self.__settings.appsize)
        self.__savesearch = customtkinter.CTkButton(
            self, width=1, text="", image=self.__settings.imagedictionary["ellipsis"], command=self.__on_search
        )
        self.__savelabel.grid(column=1, row=1)
        self.__savecheck.grid(column=2, row=1, sticky="e")

    def __set_possitions(self):
        # Column 1
        self.columnconfigure(1, weight=0)
        self.__settingsbutton.grid(column=1, row=6, padx=5, pady=5, sticky="w")

        self.__buttonframe.grid(column=1, row=7, columnspan=2, sticky="n")
        self.__ignorelabel.grid(column=1, row=9, columnspan=2)
        self.__saveframe.grid(column=1, row=10, columnspan=2)

        # Column 2
        self.columnconfigure(2, weight=0)
        self.toggle_btn.grid(column=2, row=6, pady=15)

        # Column 3
        self.columnconfigure(3, weight=1)
        self.__connectlabel.grid(column=3, row=6, sticky="we", pady=15)
        self.__listlabel.grid(column=3, row=7)

        self.rowconfigure(7, weight=1)
        if self._listchatters:
            self._listchatters.grid(column=3, row=7, columnspan=2, padx=5, sticky="w" + "e" + "n" + "s")
        self.__sizeframe.grid(column=3, row=8, sticky="w" + "e", columnspan=2, padx=5)
        self.__ignoreentry.grid(column=3, row=9, sticky="w" + "e", columnspan=2, padx=5, pady=5)
        self.__saveentry.grid(column=3, row=10, sticky="w" + "e", pady=5)

        # Column 4
        self.columnconfigure(4, weight=0)
        self._daynightbutton.grid(column=4, row=6, padx=5, pady=5, sticky="e")
        self.__savesearch.grid(column=4, row=10, padx=5, sticky="e")
