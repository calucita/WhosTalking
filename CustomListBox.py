"""Custom GUI widget for a box with labels."""
import customtkinter


class CustomListBox(customtkinter.CTkScrollableFrame):
    """Custom list box widget containing a frame with labels and a scrollbar."""

    def __init__(self, master, font, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._list = []
        self._lastcolor = False
        self._customfont = font

    def add_item(self, text: str) -> None:
        """Adds a string to the list box.

        Args:
            text (str)
        """
        color = "transparent"
        if not self._lastcolor:
            color = ("gray90", "gray25")
        self._lastcolor = not self._lastcolor
        label = customtkinter.CTkLabel(
            self, text=text, compound="left", padx=5, anchor="w", fg_color=color, corner_radius=3, font=self._customfont
        )

        label.grid(row=len(self._list), column=0, sticky="w" + "e")
        self._list.append(label)

    def delete(self, index: int) -> None:
        """Removes an entry from the list box.

        Args:
            index (int): index to delete.
        """
        if index < len(self._list):
            self.__delete_label(self._list.pop(index))

    def get(self, index: int) -> str:
        """Retrieves the text contained at an index.

        Args:
            index (int)

        Returns:
            str: stored text. Empty str if out of range.
        """
        if index >= len(self._list):
            return ""
        return self._list[index].cget("text")

    def delete_all(self):
        """Deletes all the entries in the list box"""
        while self._list:
            self.__delete_label(self._list.pop())

    def __delete_label(self, label) -> None:
        label.destroy()
        self.update()
