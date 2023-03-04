from tkinter import Tk

from ModeSelector import ModeSelector

class FontGame(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry("600x400")
        mode = ModeSelector()
        mode.pack(fill='both', expand=True, anchor='center')
    

#jogar()
root = FontGame()
root.mainloop()
