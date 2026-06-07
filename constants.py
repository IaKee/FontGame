from dataclasses import dataclass


UI_FONT = "Comic Sans MS"
BASE_ROUND_SCORE = 100

# Fontes comuns e legiveis que acompanham o Windows.
STANDARD_WINDOWS_FONTS = [
    "Arial",
    "Calibri",
    "Cambria",
    "Candara",
    "Comic Sans MS",
    "Consolas",
    "Courier New",
    "Georgia",
    "Impact",
    "Lucida Console",
    "Segoe Print",
    "Segoe UI",
    "Tahoma",
    "Times New Roman",
    "Trebuchet MS",
    "Verdana",
]

# Inclui fontes decorativas e dingbats para o fator de dificuldade 2.
ALL_WINDOWS_FONTS = STANDARD_WINDOWS_FONTS + [
    "Arial Black",
    "Bauhaus 93",
    "Bodoni MT",
    "Bookman Old Style",
    "Brush Script MT",
    "Century Gothic",
    "Cooper Black",
    "Franklin Gothic Medium",
    "Garamond",
    "Haettenschweiler",
    "Lucida Handwriting",
    "Magneto",
    "Mistral",
    "Monotype Corsiva",
    "OCR A Extended",
    "Old English Text MT",
    "Palatino Linotype",
    "Perpetua",
    "Rockwell Extra Bold",
    "Showcard Gothic",
    "Stencil",
    "Symbol",
    "Webdings",
    "Wide Latin",
    "Wingdings",
]

PHRASES = [
    "O cachorro late, a caravana passa.",
    "A pressa e inimiga da perfeicao.",
    "Quem semeia vento colhe tempestade.",
    "De grao em grao a galinha enche o papo.",
    "Quem ri por ultimo ri melhor.",
    "Agua mole em pedra dura, tanto bate ate que fura.",
    "O pior cego e o que nao quer ver.",
    "Em boca fechada nao entra mosca.",
    "A uniao faz a forca.",
    "Antes tarde do que nunca.",
    "A necessidade e a mae da invencao.",
    "Cada macaco no seu galho.",
]


@dataclass(frozen=True)
class Factor:
    key: str
    title: str
    weight: float
    choices: tuple[str, str, str]


FACTORS = (
    Factor(
        "font_size",
        "Tamanho da fonte",
        1.0,
        ("1 - Fixo", "2 - Aleatorio por palavra", "3 - Aleatorio por letra"),
    ),
    Factor(
        "colors",
        "Cores",
        1.2,
        ("1 - Cor unica", "2 - Fundo e palavras variados", "3 - Cor por letra"),
    ),
    Factor(
        "answer_fonts",
        "Fonte das alternativas",
        1.5,
        ("1 - Cada nome em sua fonte", "2 - Comic Sans em todas", "3 - Fontes aleatorias"),
    ),
    Factor(
        "example_time",
        "Exibicao do exemplo",
        1.6,
        ("1 - Infinito", "2 - 5 segundos", "3 - 0,5 segundo"),
    ),
    Factor(
        "answer_time",
        "Tempo para responder",
        2.0,
        ("1 - 15 segundos", "2 - 8 segundos", "3 - 15 a 3 segundos"),
    ),
    Factor(
        "font_pool",
        "Fontes utilizadas",
        1.3,
        ("1 - Windows legiveis", "2 - Todas do Windows", "3 - Todas instaladas"),
    ),
)


def score_per_hit(settings):
    weighted_difficulty = sum(
        factor.weight * (settings[factor.key] - 1) / 2 for factor in FACTORS
    )
    maximum = sum(factor.weight for factor in FACTORS)
    return round(BASE_ROUND_SCORE * (1 + 4 * weighted_difficulty / maximum))


def round_time_seconds(settings, hits):
    level = settings["answer_time"]
    if level == 1:
        return 15.0
    if level == 2:
        return 8.0
    return max(3.0, 15.0 - hits * 0.6)