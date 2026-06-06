from tkinter import Frame, IntVar, StringVar
from tkinter.ttk import Button, Label, Radiobutton


class ModeSelector(Frame):
    def __init__(self, master, on_start_game):
        Frame.__init__(self, master)

        self.on_start_game = on_start_game

        self.title = Label(
            self,
            text="Bem-vindo ao jogo de identificação de fontes padrão do Windows!",
        )
        self.title.pack(padx=5, pady=(35, 10))

        self.mode_title = Label(self, text="Selecione o modo de jogo:")
        self.mode_title.pack()

        self.mode_frame = Frame(self)
        self.selected_mode = StringVar(self.mode_frame, value="choose")

        self.choose_option = Radiobutton(
            master=self.mode_frame,
            text="Escolher entre opções",
            variable=self.selected_mode,
            value="choose",
        )
        self.choose_option.pack(side="left", padx=5)

        self.type_option = Radiobutton(
            master=self.mode_frame,
            text="Digitar resposta",
            variable=self.selected_mode,
            value="type",
        )
        self.type_option.pack(side="left", padx=5)

        self.mode_frame.pack(pady=(0, 12))

        self.difficulty_title = Label(master=self, text="Selecione a dificuldade:")
        self.difficulty_title.pack()

        self.difficulty_frame = Frame(self)
        self.selected_difficulty = IntVar(self.difficulty_frame, value=0)

        self.easy = Radiobutton(
            master=self.difficulty_frame,
            variable=self.selected_difficulty,
            text="Fácil",
            value=0,
        )
        self.easy.pack(side="left", padx=5)

        self.medium = Radiobutton(
            master=self.difficulty_frame,
            variable=self.selected_difficulty,
            text="Médio",
            value=1,
        )
        self.medium.pack(side="left", padx=5)

        self.hard = Radiobutton(
            master=self.difficulty_frame,
            variable=self.selected_difficulty,
            text="Difícil",
            value=2,
        )
        self.hard.pack(side="left", padx=5)

        self.difficulty_frame.pack(pady=(0, 15))

        self.button_frame = Frame(self)

        self.ok_button = Button(
            master=self.button_frame,
            text="Começar",
            command=self.start_game,
        )
        self.ok_button.pack(side="left")

        self.cancel_button = Button(
            master=self.button_frame,
            text="Cancelar",
            command=self.master.destroy,
        )
        self.cancel_button.pack(padx=(5, 0), side="left")

        self.button_frame.pack(pady=(0, 5))

    def start_game(self):
        self.on_start_game(
            self.selected_mode.get(),
            self.selected_difficulty.get(),
        )
