from tkinter import Button, Frame, IntVar, Label, Radiobutton

from constants import FACTORS, UI_FONT, score_per_hit


class ModeSelectorFrame(Frame):
    def __init__(self, master, on_start, **kwargs):
        super().__init__(master, bg="#f6f0ff", **kwargs)
        self.on_start = on_start
        self.variables = {
            factor.key: IntVar(self, value=1)
            for factor in FACTORS
        }

        Label(
            self,
            text="FontGame",
            font=(UI_FONT, 30, "bold"),
            bg=self["bg"],
            fg="#30204f",
        ).pack(pady=(22, 2))
        Label(
            self,
            text="Monte sua dificuldade. O jogo continua ate voce errar ou o tempo acabar.",
            font=(UI_FONT, 11),
            bg=self["bg"],
            fg="#594d70",
        ).pack(pady=(0, 14))

        factors_frame = Frame(self, bg=self["bg"])
        factors_frame.pack(fill="both", expand=True, padx=28)

        for row, factor in enumerate(FACTORS):
            Label(
                factors_frame,
                text=f"{factor.title}  (peso {factor.weight:g})",
                font=(UI_FONT, 11, "bold"),
                bg=self["bg"],
                anchor="w",
            ).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=7)
            for column, choice in enumerate(factor.choices, start=1):
                Radiobutton(
                    factors_frame,
                    text=choice,
                    variable=self.variables[factor.key],
                    value=column,
                    command=self.update_score,
                    font=(UI_FONT, 9),
                    bg=self["bg"],
                    activebackground=self["bg"],
                    selectcolor="#e6dcfa",
                    anchor="w",
                ).grid(row=row, column=column, sticky="w", padx=5)

        self.score_label = Label(
            self,
            font=(UI_FONT, 13, "bold"),
            bg=self["bg"],
            fg="#3455db",
        )
        self.score_label.pack(pady=10)

        Button(
            self,
            text="Comecar jogo infinito",
            command=self.confirm,
            font=(UI_FONT, 14, "bold"),
            bg="#3455db",
            fg="white",
            activebackground="#243da8",
            activeforeground="white",
            relief="flat",
            padx=24,
            pady=8,
        ).pack(pady=(0, 22))
        self.update_score()

    def settings(self):
        return {key: variable.get() for key, variable in self.variables.items()}

    def update_score(self):
        self.score_label.configure(
            text=f"Cada acerto vale {score_per_hit(self.settings())} pontos"
        )

    def confirm(self):
        self.on_start(self.settings())
