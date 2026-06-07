import colorsys
import random
from time import perf_counter
from tkinter import Button, Canvas, Frame, Label, Tk, font as tkfont

from constants import (
    ALL_WINDOWS_FONTS,
    PHRASES,
    STANDARD_WINDOWS_FONTS,
    UI_FONT,
    round_time_seconds,
    score_per_hit,
)
from mode_selector_frame import ModeSelectorFrame


def mix_color(start, end, amount):
    values = tuple(
        round(start[index] + (end[index] - start[index]) * amount)
        for index in range(3)
    )
    return "#%02x%02x%02x" % values


def contrasting_color(background, close=False):
    red, green, blue = tuple(
        int(background[index : index + 2], 16) / 255
        for index in (1, 3, 5)
    )
    hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
    if close:
        value = value - 0.18 if value > 0.5 else value + 0.18
        saturation = min(1.0, saturation + 0.15)
    else:
        value = 0.12 if value > 0.5 else 0.92
        saturation = max(0.25, saturation)
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return "#%02x%02x%02x" % tuple(round(channel * 255) for channel in rgb)


def random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


class FontGame(Tk):
    def __init__(self, _lang=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("FontGame")
        self.geometry("900x650")
        self.minsize(760, 560)
        self.option_add("*Font", (UI_FONT, 10))
        self.screen = None
        self.timer_job = None
        self.example_job = None
        self.settings = {}
        self.history = []
        self.score = 0
        self.selected = None
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.show_settings()

    def clear_screen(self):
        for job in (self.timer_job, self.example_job):
            if job:
                self.after_cancel(job)
        self.timer_job = None
        self.example_job = None
        if self.screen:
            self.screen.destroy()

    def show_settings(self):
        self.clear_screen()
        self.screen = ModeSelectorFrame(self, self.start_game)
        self.screen.pack(fill="both", expand=True)

    def start_game(self, settings):
        self.settings = settings
        self.history = []
        self.score = 0
        self.next_round()

    def font_pool(self):
        installed = sorted(set(tkfont.families(self)))
        level = self.settings["font_pool"]
        requested = STANDARD_WINDOWS_FONTS if level == 1 else ALL_WINDOWS_FONTS
        pool = installed if level == 3 else [font for font in requested if font in installed]
        clean_fallback = [
            font for font in installed
            if not font.startswith("@") and len(font) > 2
        ]
        return pool if len(pool) >= 6 else clean_fallback

    def next_round(self):
        self.clear_screen()
        self.selected = None
        pool = self.font_pool()
        self.correct_font = random.choice(pool)
        self.phrase = random.choice(PHRASES)
        self.options = random.sample(
            [font for font in pool if font != self.correct_font], 5
        ) + [self.correct_font]
        random.shuffle(self.options)
        self.round_duration = round_time_seconds(self.settings, len(self.history))
        self.round_started = perf_counter()

        self.screen = Frame(self, bg="#f7f7fb")
        self.screen.pack(fill="both", expand=True)
        self.progress = Canvas(
            self.screen, height=9, bg="#f7f7fb", highlightthickness=0, bd=0
        )
        self.progress.pack(fill="x")

        info = Frame(self.screen, bg="#f7f7fb")
        info.pack(fill="x", padx=24, pady=(12, 4))
        Label(
            info, text=f"Pontos: {self.score}", bg="#f7f7fb",
            font=(UI_FONT, 13, "bold")
        ).pack(side="left")
        self.time_label = Label(
            info, bg="#f7f7fb", font=(UI_FONT, 13, "bold")
        )
        self.time_label.pack(side="right")

        Label(
            self.screen,
            text="Qual e a fonte da frase abaixo?",
            bg="#f7f7fb",
            fg="#413b51",
            font=(UI_FONT, 15, "bold"),
        ).pack(pady=(8, 5))

        self.example = Canvas(
            self.screen, height=170, bg="#ffffff", highlightthickness=0, bd=0
        )
        self.example.pack(fill="x", padx=24, pady=(0, 16))
        self.example.bind("<Configure>", lambda _event: self.draw_phrase())
        self.draw_phrase()

        options_frame = Frame(self.screen, bg="#f7f7fb")
        options_frame.pack(fill="both", expand=True, padx=24)
        self.option_buttons = []
        for index, option in enumerate(self.options):
            button = Button(
                options_frame,
                text=option,
                command=lambda value=option: self.mark_option(value),
                font=self.answer_font(option, pool),
                bg="#ffffff",
                fg="#272331",
                activebackground="#e8e4ff",
                relief="flat",
                bd=0,
                pady=12,
            )
            button.grid(
                row=index // 2, column=index % 2, sticky="nsew", padx=7, pady=6
            )
            options_frame.grid_columnconfigure(index % 2, weight=1)
            options_frame.grid_rowconfigure(index // 2, weight=1)
            self.option_buttons.append(button)

        self.confirm_button = Button(
            self.screen,
            text="Selecione uma alternativa",
            command=self.confirm_selection,
            state="disabled",
            font=(UI_FONT, 13, "bold"),
            bg="#3455db",
            disabledforeground="#8a8792",
            fg="white",
            relief="flat",
            padx=22,
            pady=8,
        )
        self.confirm_button.pack(pady=(10, 18))
        self.bind("<Return>", self.confirm_selection)
        self.bind("<KP_Enter>", self.confirm_selection)

        display_seconds = {1: None, 2: 5_000, 3: 500}[self.settings["example_time"]]
        if display_seconds:
            self.example_job = self.after(display_seconds, self.hide_example)
        self.update_timer()

    def answer_font(self, option, pool):
        level = self.settings["answer_fonts"]
        if level == 1:
            return (option, 12)
        if level == 2:
            return (UI_FONT, 12)
        return (random.choice(pool), 12)

    def mark_option(self, option):
        self.selected = option
        for button, value in zip(self.option_buttons, self.options):
            selected = value == option
            button.configure(
                bg="#dcd4ff" if selected else "#ffffff",
                relief="solid" if selected else "flat",
                bd=2 if selected else 0,
            )
        self.confirm_button.configure(
            text="Confirmar resposta", state="normal", disabledforeground="white"
        )

    def confirm_selection(self, _event=None):
        if not self.selected:
            return
        elapsed = perf_counter() - self.round_started
        if self.selected != self.correct_font:
            self.game_over(f"Resposta incorreta. A fonte era {self.correct_font}.")
            return
        points = score_per_hit(self.settings)
        self.score += points
        self.history.append(
            {
                "phrase": self.phrase,
                "font": self.correct_font,
                "seconds": elapsed,
                "points": points,
            }
        )
        self.next_round()

    def update_timer(self):
        elapsed = perf_counter() - self.round_started
        remaining = max(0.0, self.round_duration - elapsed)
        ratio = remaining / self.round_duration
        self.time_label.configure(text=f"{remaining:04.1f}s")
        self.progress.delete("all")
        width = self.progress.winfo_width()
        color = mix_color((226, 54, 74), (44, 104, 232), ratio)
        self.progress.create_rectangle(
            0, 0, width * ratio, 9, fill=color, outline=""
        )
        if remaining <= 0:
            self.game_over("O tempo acabou.")
            return
        self.timer_job = self.after(33, self.update_timer)

    def hide_example(self):
        self.example_job = None
        self.example.delete("all")
        self.example.create_text(
            self.example.winfo_width() / 2,
            85,
            text="Exemplo oculto",
            fill="#77717f",
            font=(UI_FONT, 16, "italic"),
        )

    def draw_phrase(self):
        if not hasattr(self, "phrase") or self.example_job is None and not self.example.find_all():
            pass
        canvas = self.example
        canvas.delete("all")
        colors_level = self.settings.get("colors", 1)
        background = random_color() if colors_level >= 2 else "#ffffff"
        canvas.configure(bg=background)

        tokens = list(self.phrase) if self.settings.get("font_size") == 3 or colors_level == 3 else self.phrase.split(" ")
        separator = "" if len(tokens) == len(self.phrase) else " "
        sizes = []
        for _token in tokens:
            level = self.settings.get("font_size", 1)
            sizes.append(48 if level == 1 else random.randint(28, 58))
        fonts = [tkfont.Font(family=self.correct_font, size=size) for size in sizes]
        widths = [font.measure(token + separator) for font, token in zip(fonts, tokens)]
        total_width = sum(widths)
        max_width = max(100, canvas.winfo_width() - 30)
        scale = min(1.0, max_width / max(total_width, 1))
        if scale < 1:
            fonts = [
                tkfont.Font(family=self.correct_font, size=max(12, round(size * scale)))
                for size in sizes
            ]
            widths = [font.measure(token + separator) for font, token in zip(fonts, tokens)]
            total_width = sum(widths)

        x = max(15, (canvas.winfo_width() - total_width) / 2)
        shared_color = contrasting_color(background)
        for token, font, width in zip(tokens, fonts, widths):
            if colors_level == 1:
                color = shared_color
            elif colors_level == 2:
                color = contrasting_color(background)
            else:
                color = contrasting_color(background, close=random.choice((True, False)))
            canvas.create_text(
                x, 85, text=token + separator, anchor="w", font=font, fill=color
            )
            x += width

    def game_over(self, reason):
        self.clear_screen()
        self.unbind("<Return>")
        self.unbind("<KP_Enter>")
        self.screen = Frame(self, bg="#211b2f")
        self.screen.pack(fill="both", expand=True)
        installed = self.font_pool()

        title = Frame(self.screen, bg="#211b2f")
        title.pack(pady=(26, 4))
        for word in ("GAME", "OVER"):
            Label(
                title,
                text=word,
                font=(random.choice(installed), 30, "bold"),
                bg="#211b2f",
                fg=random.choice(("#ff5c70", "#82aaff", "#f7d774")),
            ).pack(side="left", padx=8)

        Label(
            self.screen,
            text=reason,
            font=(random.choice(installed), 13),
            bg="#211b2f",
            fg="#eee9f8",
        ).pack(pady=4)
        Label(
            self.screen,
            text=f"{self.score} pontos | {len(self.history)} acertos",
            font=(random.choice(installed), 18, "bold"),
            bg="#211b2f",
            fg="#ffffff",
        ).pack(pady=(4, 12))

        history_frame = Frame(self.screen, bg="#302842")
        history_frame.pack(fill="both", expand=True, padx=30, pady=8)
        if not self.history:
            Label(
                history_frame,
                text="Nenhum acerto nesta partida.",
                font=(random.choice(installed), 13),
                bg="#302842",
                fg="#ddd5e9",
            ).pack(pady=24)
        for index, hit in enumerate(self.history, start=1):
            text = (
                f"{index}. {hit['phrase']}  |  {hit['font']}  |  "
                f"{hit['seconds']:.2f}s  |  +{hit['points']}"
            )
            Label(
                history_frame,
                text=text,
                font=(random.choice(installed), 10),
                bg="#302842",
                fg="#f3eff9",
                anchor="w",
            ).pack(fill="x", padx=14, pady=4)

        buttons = Frame(self.screen, bg="#211b2f")
        buttons.pack(pady=18)
        Button(
            buttons, text="Jogar novamente", command=lambda: self.start_game(self.settings),
            font=(UI_FONT, 12, "bold"), bg="#3455db", fg="white", relief="flat", padx=14
        ).pack(side="left", padx=6)
        Button(
            buttons, text="Mudar dificuldade", command=self.show_settings,
            font=(UI_FONT, 12, "bold"), bg="#5d536e", fg="white", relief="flat", padx=14
        ).pack(side="left", padx=6)