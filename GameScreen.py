from random import choice, sample, shuffle
from tkinter import Frame, StringVar, font
from tkinter.ttk import Button, Entry, Label

from constants import OPTION_COUNT_BY_DIFFICULTY, PHRASES, PREFERRED_FONTS, ROUNDS_PER_GAME

try:
    import winsound
except ImportError:
    winsound = None


class GameScreen(Frame):
    def __init__(self, master, mode, difficulty, on_back_to_menu):
        Frame.__init__(self, master)

        self.mode = mode
        self.difficulty = difficulty
        self.on_back_to_menu = on_back_to_menu
        self.round_number = 0
        self.score = 0
        self.current_font = None
        self.current_phrase = ""
        self.round_answered = False
        self.answer = StringVar()
        self.phrase_font = font.Font(family="Segoe UI", size=24)

        self.available_fonts = self.get_available_fonts()

        self.header = Label(self)
        self.header.pack(padx=10, pady=(15, 5), fill="x")

        self.phrase_box = Frame(self, borderwidth=1, relief="solid")
        self.phrase_box.pack_propagate(False)
        self.phrase_box.pack(pady=12)

        self.phrase_label = Label(
            self.phrase_box,
            anchor="center",
            justify="center",
            font=self.phrase_font,
        )
        self.phrase_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.answer_frame = Frame(self)
        self.answer_frame.pack(padx=10, pady=5, fill="x")

        self.feedback = Label(self)
        self.feedback.pack(padx=10, pady=10, fill="x")

        self.footer_frame = Frame(self)
        self.footer_frame.pack(pady=(10, 15))

        self.next_button = Button(
            self.footer_frame,
            text="Próxima",
            command=self.next_round,
            width=10,
        )
        self.menu_button = Button(
            self.footer_frame,
            text="Menu",
            command=self.on_back_to_menu,
            width=10,
        )
        self.menu_button.pack(side="left", padx=5)

        self.bind("<Configure>", self.resize_phrase_box)
        self.next_round()

    def get_available_fonts(self):
        installed_fonts = set(font.families())
        available_fonts = [font_name for font_name in PREFERRED_FONTS if font_name in installed_fonts]

        if len(available_fonts) >= 3:
            return available_fonts

        return sorted(installed_fonts)

    def clear_answers(self):
        for child in self.answer_frame.winfo_children():
            child.destroy()

        self.next_button.pack_forget()
        self.feedback.config(text="")
        self.answer.set("")

    def next_round(self):
        if self.round_number >= ROUNDS_PER_GAME:
            self.show_result()
            return

        self.clear_answers()
        self.round_number += 1
        self.round_answered = False

        self.current_phrase = choice(PHRASES)
        self.current_font = choice(self.available_fonts)

        self.header.config(
            text=f"Rodada {self.round_number}/{ROUNDS_PER_GAME} | Pontuação: {self.score}"
        )
        self.phrase_font.configure(family=self.current_font)
        self.phrase_label.config(text=self.current_phrase)
        self.resize_phrase_box()

        if self.mode == "type":
            self.show_type_answer()
        else:
            self.show_choice_answer()

    def show_choice_answer(self):
        option_count = min(
            OPTION_COUNT_BY_DIFFICULTY.get(self.difficulty, 3),
            len(self.available_fonts),
        )

        wrong_fonts = [font_name for font_name in self.available_fonts if font_name != self.current_font]
        options = sample(wrong_fonts, option_count - 1) + [self.current_font]
        shuffle(options)

        for option in options:
            button = Button(
                self.answer_frame,
                text=option,
                command=lambda selected=option: self.check_answer(selected),
            )
            button.pack(pady=3, fill="x")

    def show_type_answer(self):
        label = Label(self.answer_frame, text="Digite o nome da fonte:")
        label.pack(pady=(0, 5))

        entry = Entry(self.answer_frame, textvariable=self.answer, width=32)
        entry.pack(pady=(0, 8))
        entry.focus_set()
        entry.bind("<Return>", lambda _event: self.check_answer(self.answer.get()))

        confirm = Button(
            self.answer_frame,
            text="Confirmar",
            command=lambda: self.check_answer(self.answer.get()),
        )
        confirm.pack()

    def check_answer(self, selected_font):
        if self.round_answered:
            return

        self.round_answered = True
        selected_font = selected_font.strip()
        is_correct = selected_font.lower() == self.current_font.lower()

        for child in self.answer_frame.winfo_children():
            child.configure(state="disabled")

        if is_correct:
            self.score += 1
            self.feedback.config(text="Acertou!")
            self.play_correct_sound()
        else:
            self.feedback.config(text=f"Errou. A fonte correta era {self.current_font}.")
            self.play_wrong_sound()

        self.header.config(
            text=f"Rodada {self.round_number}/{ROUNDS_PER_GAME} | Pontuação: {self.score}"
        )
        self.next_button.pack(side="left", padx=5)

    def play_correct_sound(self):
        if winsound is not None:
            winsound.Beep(880, 120)
            winsound.Beep(1175, 140)
        else:
            self.bell()

    def play_wrong_sound(self):
        if winsound is not None:
            winsound.Beep(220, 180)
            winsound.Beep(165, 220)
        else:
            self.bell()

    def show_result(self):
        self.clear_answers()
        self.header.config(text="Fim de jogo")
        self.current_font = "Segoe UI"
        self.current_phrase = f"Você acertou {self.score} de {ROUNDS_PER_GAME} fontes."
        self.phrase_font.configure(family=self.current_font)
        self.phrase_label.config(text=self.current_phrase)
        self.resize_phrase_box()
        self.feedback.config(text="")

        play_again = Button(self.answer_frame, text="Jogar novamente", command=self.restart)
        play_again.pack(pady=5)

    def restart(self):
        self.round_number = 0
        self.score = 0
        self.next_round()

    def resize_phrase_box(self, _event=None):
        width = max(int(self.winfo_width() * 0.88), 320)
        height = max(int(self.winfo_height() * 0.28), 120)

        self.phrase_box.config(width=width, height=height)
        self.phrase_label.config(wraplength=max(width - 24, 80))
        self.adjust_phrase_font(width - 24, height - 24)

    def adjust_phrase_font(self, max_width, max_height):
        if not self.current_phrase or not self.current_font:
            return

        low = 8
        high = max(12, min(int(max_height * 0.65), int(max_width * 0.12)))
        best = low

        while low <= high:
            middle = (low + high) // 2
            self.phrase_font.configure(family=self.current_font, size=middle)

            if self.phrase_fits(max_width, max_height):
                best = middle
                low = middle + 1
            else:
                high = middle - 1

        self.phrase_font.configure(family=self.current_font, size=best)

    def phrase_fits(self, max_width, max_height):
        lines = self.wrap_phrase(max_width)
        line_height = self.phrase_font.metrics("linespace")
        text_height = line_height * len(lines)
        widest_line = max((self.phrase_font.measure(line) for line in lines), default=0)

        return text_height <= max_height and widest_line <= max_width

    def wrap_phrase(self, max_width):
        lines = []

        for paragraph in self.current_phrase.splitlines() or [""]:
            words = paragraph.split()
            line = ""

            for word in words:
                candidate = f"{line} {word}".strip()

                if self.phrase_font.measure(candidate) <= max_width:
                    line = candidate
                else:
                    if line:
                        lines.append(line)
                    lines.extend(self.break_long_word(word, max_width))
                    line = ""

            if line:
                lines.append(line)

        return lines or [""]

    def break_long_word(self, word, max_width):
        pieces = []
        piece = ""

        for character in word:
            candidate = f"{piece}{character}"

            if self.phrase_font.measure(candidate) <= max_width:
                piece = candidate
            else:
                if piece:
                    pieces.append(piece)
                piece = character

        if piece:
            pieces.append(piece)

        return pieces
