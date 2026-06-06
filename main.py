from tkinter import Tk

from GameScreen import GameScreen
from ModeSelector import ModeSelector


class FontGame(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Font Game")
        self.set_initial_size()
        self.current_screen = None

        self.show_mode_selector()

    def set_initial_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = max(int(screen_width * 0.42), 520)
        window_height = max(int(screen_height * 0.58), 500)

        self.geometry(f"{window_width}x{window_height}")
        self.minsize(420, 420)
        self.resizable(True, True)

    def set_screen(self, screen):
        if self.current_screen is not None:
            self.current_screen.destroy()

        self.current_screen = screen
        self.current_screen.pack(fill="both", expand=True)

    def show_mode_selector(self):
        self.set_screen(ModeSelector(self, self.show_game))

    def show_game(self, mode, difficulty):
        self.set_screen(GameScreen(self, mode, difficulty, self.show_mode_selector))


if __name__ == "__main__":
    root = FontGame()
    root.mainloop()
