"""Handler of keyring stored information"""
import typing
import hashlib
import keyring
import customtkinter

# This is for windows... ... might generalize later...
from keyrings.alt import Windows

from AppInfo import SERVICE_O, SERVICE, SERVAR


class CredentialsSettings:
    """Handler and host of keyring information."""

    __savef: str = "saveFile"

    def __init__(self) -> None:
        self.savevar = customtkinter.StringVar()
        self.namevar = customtkinter.StringVar()
        self.channelvar = customtkinter.StringVar()
        self.oauthvar = customtkinter.StringVar()
        keyring.set_keyring(Windows.RegistryKeyring())

    def load_data(self) -> None:
        """Loads data into the vars."""
        self.__load_savefile()
        self.__load_credentials()

    def __load_savefile(self):
        filename = self.get_save_file_from_key()
        if filename:
            self.savevar.set(filename)

    def __load_credentials(self) -> typing.Union[dict, None]:
        legacy = False
        if self.__get_password(isold=True):
            legacy = True

        botto = self.__get_password(isold=legacy)
        if not botto:
            return None
        self.namevar.set(botto)

        username = botto
        if not legacy:
            username = SERVICE_O
        channel = self.__get_password(username, legacy)
        if not channel:
            return None
        self.channelvar.set(channel)

        username = botto + channel
        if not legacy:
            username = botto
        oauth = self.__get_password(username, legacy)
        if not oauth:
            return None
        self.oauthvar.set(oauth)

        if legacy:
            self.__do_legacy_clean()

    def save_credentials(self):
        """Stores the var data into the keyring."""
        if self.namevar.get() and self.channelvar.get() and self.oauthvar.get():
            keyring.set_password(SERVICE, SERVAR, self.namevar.get())
            keyring.set_password(SERVICE, self.__process_hash(self.namevar.get()), self.oauthvar.get())
            keyring.set_password(SERVICE, self.__process_hash(SERVICE_O), self.channelvar.get())

    def save_file_in_key(self):
        """Stores save file path."""
        if self.get_save_file_from_key() != self.savevar.get():
            keyring.set_password(SERVICE, self.__savef, self.savevar.get())

    def get_save_file_from_key(self):
        """Retrieves save file path."""
        return keyring.get_password(SERVICE, self.__savef)

    def __process_hash(self, string: str = "") -> str:
        return hashlib.sha256((SERVAR + string).encode("ascii")).hexdigest()

    def __get_password(self, username: str = "", isold: bool = False) -> typing.Union[str, None]:
        service = SERVICE_O
        if not isold:
            service = SERVICE

        if not username:
            username = service
        elif not isold:
            username = self.__process_hash(username)

        return keyring.get_password(service, username)

    def __do_legacy_clean(self) -> None:
        keyring.delete_password(SERVICE_O, SERVICE_O)
        keyring.delete_password(SERVICE_O, self.namevar.get())
        keyring.delete_password(SERVICE_O, self.namevar.get() + self.channelvar.get())

        self.save_credentials()
