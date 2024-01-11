"""Utils for handling settings controlling the GUI"""
import configparser
from os import path
from typing import Tuple
import customtkinter
from PIL import Image


class GUISettings:
    """GUI settings retriever"""

    def __init__(self):
        self.__imagelist: dict[str, list[Image.Image]] = {}
        self.imagedictionary: dict[str, customtkinter.CTkImage] = {}
        self.appsize = customtkinter.CTkFont(size=13)
        self.apphighlightedsize = customtkinter.CTkFont(size=14)
        self.customfont = customtkinter.CTkFont(size=13)
        self.themevar = customtkinter.StringVar()
        self.joinreplyvar = customtkinter.IntVar()
        self.__load_settings()

    def delete_images(self, prefix: str):
        """Destroys the loaded images for a window (prefix).

        Args:
            prefix (str): window specifier.
        """
        if prefix not in self.__imagelist:
            return
        for image in self.__imagelist[prefix]:
            image.close()

    def import_images(self, prefix: str):
        """Loads the images for a window (prefix)

        Args:
            prefix (str): window specifier.
        """
        ext = ".png"
        listofimg = [
            "main-moon.png",
            "main-lightbulb.png",
            "main-stop.png",
            "main-play.png",
            "main-dice.png",
            "main-lupa-plus.png",
            "main-lupa-minus.png",
            "main-trash-can.png",
            "main-ellipsis.png",
            "main-filter.png",
            "main-gear.png",
            "main-reply.png",
            "set-minus.png",
            "set-plus.png",
            "set-text-height.png",
            "set-text-height-dark.png",
            "set-refresh.png",
        ]
        for file in listofimg:
            if file.startswith(prefix) and file.endswith(ext) and not file.endswith("-dark.png"):
                file = file.removesuffix(ext)
                name = file.removeprefix(prefix)
                self.__add_image_to_dict(prefix, name, file)
            else:
                continue
        self.__update_image_sizes()

    def __add_image_to_dict(self, prefix: str, name: str, file: str, size: Tuple[int, int] = (15, 15)):
        imgdark = Image.open(path.join(path.dirname(__file__), "./img/" + file + ".png"))
        if prefix not in self.__imagelist:
            self.__imagelist[prefix] = []
        self.__imagelist[prefix].append(imgdark)
        pathlight = path.join(path.dirname(__file__), "./img/" + file + "-dark.png")
        if path.exists(pathlight):
            imglight = Image.open(pathlight)
            self.__imagelist[prefix].append(imglight)
            self.imagedictionary[name] = customtkinter.CTkImage(imglight, imgdark, size=size)
        else:
            self.imagedictionary[name] = customtkinter.CTkImage(imgdark, size=size)

    def __update_image_sizes(self):
        size = self.appsize["size"]
        for name, image in self.imagedictionary.items():
            if name == "dice":
                image.configure(size=(size + 7, size + 7))
            else:
                image.configure(size=(size + 2, size + 2))

    def change_app_font_size(self, isup: bool) -> None:
        """Change the app font size globally one tick up or down.

        Args:
            isup (bool): True for larger font; False for smaller.
        """
        self.__change_font_size(self.appsize, isup)
        self.__change_font_size(self.apphighlightedsize, isup)
        self.change_list_font_size(isup)
        self.__update_image_sizes()

        self.save_settings()

    def set_font_size(self, size: int = 13) -> None:
        """Sets the global font size to the specified value.

        Args:
            size (int, optional): Defaults to 13.
        """
        self.appsize.configure(size=size)
        self.apphighlightedsize.configure(size=size + 1)
        self.customfont.configure(size=size)
        self.__update_image_sizes()

        self.save_settings()

    def __change_font_size(self, font: customtkinter.CTkFont, isup: bool):
        if isup:
            font.configure(size=font["size"] + 1)
        else:
            font.configure(size=font["size"] - 1)

    def change_list_font_size(self, isup: bool) -> None:
        """changes the font size of the list of chatters.

        Args:
            isup (bool): _description_
        """
        self.__change_font_size(self.customfont, isup)
        self.save_settings()

    #############################################################
    ############ GUI configuration

    # save all gui elements into an ini file
    def save_settings(self, settings_name="settings"):
        """Saves the active settings for the GUI.

        Args:
            settings_name (str, optional): File name. Defaults to "settings".
        """
        config = configparser.ConfigParser()

        config[settings_name] = {
            "app_size": str(self.appsize["size"]),
            "font_size": str(self.customfont["size"]),
            "reply": str(self.joinreplyvar.get()),
            "theme": str(customtkinter.get_appearance_mode()).lower(),
        }
        with open(settings_name + ".ini", "w") as configfile:
            config.write(configfile)

    # load all gui elements from an ini file
    def __load_settings(self, settings_name="settings"):
        try:
            config = configparser.ConfigParser()
            filename = settings_name + ".ini"
            if path.exists(filename):
                config.read(filename)
                if "app_size" in config[settings_name]:
                    self.appsize.configure(size=int(config[settings_name]["app_size"]))
                    self.apphighlightedsize.configure(size=int(config[settings_name]["app_size"]) + 1)
                    self.__update_image_sizes()
                if "font_size" in config[settings_name]:
                    self.customfont.configure(size=int(config[settings_name]["font_size"]))
                if "reply" in config[settings_name]:
                    self.joinreplyvar.set(int(config[settings_name]["reply"]))
                if "theme" in config[settings_name]:
                    self.themevar.set(config[settings_name]["theme"])

        except Exception as e:
            print("Error on reading settings.ini. Maybe save it first." + str(e))
