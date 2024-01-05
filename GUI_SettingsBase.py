import customtkinter
import configparser
from os import path
from PIL import Image
from typing import Tuple


class GUI_SettingsBase:
    def __init__(self):
        self._ImageList: dict[str, list[Image.Image]] = {}
        self.ImageDictionary: dict[str, customtkinter.CTkImage] = {}
        self._AppSize = customtkinter.CTkFont(size=13)
        self._AppHighlightedSize = customtkinter.CTkFont(size=14)
        self._customFont = customtkinter.CTkFont(size=13)
        self.JoinReplyVar = customtkinter.IntVar()
        self.NameVar = customtkinter.StringVar()
        self.ChannelVar = customtkinter.StringVar()
        self.OauthVar = customtkinter.StringVar()
        self.load_setting()

    def delete_images(self, prefix: str):
        if prefix not in self._ImageList:
            return
        for image in self._ImageList[prefix]:
            image.close()

    def import_images(self, prefix: str):
        dirname = "./img/"
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
        imgDark = Image.open(path.join(path.dirname(__file__), "./img/" + file + ".png"))
        if prefix not in self._ImageList:
            self._ImageList[prefix] = []
        self._ImageList[prefix].append(imgDark)
        pathLight = path.join(path.dirname(__file__), "./img/" + file + "-dark.png")
        if path.exists(pathLight):
            imgLight = Image.open(pathLight)
            self._ImageList[prefix].append(imgLight)
            self.ImageDictionary[name] = customtkinter.CTkImage(imgLight, imgDark, size=size)
        else:
            self.ImageDictionary[name] = customtkinter.CTkImage(imgDark, size=size)

    def __update_image_sizes(self):
        size = self._AppSize["size"]
        for image in self.ImageDictionary:
            if image == "dice":
                self.ImageDictionary[image].configure(size=(size + 7, size + 7))
            else:
                self.ImageDictionary[image].configure(size=(size + 2, size + 2))

    def app_settings_font_plus(self):
        self.change_app_font_size(True)

    def app_settings_font_minus(self):
        self.change_app_font_size(False)

    def change_app_font_size(self, _isUp: bool) -> None:
        self.__change_font_size(self._AppSize, _isUp)
        self.__change_font_size(self._AppHighlightedSize, _isUp)
        self.change_list_font_size(_isUp)
        self.__update_image_sizes()

        self.save_setting()

    def set_font_size(self, size: int = 13) -> None:
        self._AppSize.configure(size=size)
        self._AppHighlightedSize.configure(size=size + 1)
        self._customFont.configure(size=size)
        self.__update_image_sizes()

        self.save_setting()

    def __change_font_size(self, font: customtkinter.CTkFont, _isUp: bool):
        if _isUp:
            font.configure(size=font["size"] + 1)
        else:
            font.configure(size=font["size"] - 1)

    def change_list_font_size(self, _isUp: bool) -> None:
        self.__change_font_size(self._customFont, _isUp)
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

        except Exception as e:
            print("Error on reading settings.ini. Maybe save it first." + str(e))
            pass
