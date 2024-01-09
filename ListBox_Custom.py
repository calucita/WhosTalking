import customtkinter


class ListBox_Custom(customtkinter.CTkScrollableFrame):
    def __init__(self, master, font, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._list = []
        self._lastColor = False
        self._customfont = font

    def add_item(self, text: str) -> None:
        color = "transparent"
        if not self._lastColor:
            color = ("gray90", "gray25")
        self._lastColor = not self._lastColor
        label = customtkinter.CTkLabel(
            self, text=text, compound="left", padx=5, anchor="w", fg_color=color, corner_radius=3, font=self._customfont
        )

        label.grid(row=len(self._list), column=0, sticky="w" + "e")
        self._list.append(label)

    def delete(self, index: int) -> None:
        if index < len(self._list):
            self.__delete_label(self._list.pop(index))

    def get(self, index: int) -> str:
        if index >= len(self._list):
            return ""
        return self._list[index].cget("text")

    def deleteAll(self):
        while self._list:
            self.__delete_label(self._list.pop())

    def __delete_label(self, label) -> None:
        label.destroy()
        self.update()
