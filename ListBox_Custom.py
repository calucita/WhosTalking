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

    def remove_item(self, text: str) -> None:
        for label in self._list:
            if text == label.cget("text"):
                label.destroy()
                self._list.remove(label)
                return

    def delete(self, index: int) -> None:
        if index < len(self._list):
            label = self._list[index]
            label.destroy()
            self._list.remove(label)

    def get(self, index: int) -> str:
        if index >= len(self._list):
            return ""
        return self._list[index].cget("text")

    def deleteAll(self):
        while self._list:
            label = self._list.pop()
            label.destroy()
