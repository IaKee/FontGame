from random import choice, randint
import sys
from time import perf_counter, time

from tkinter import Tk, Frame, IntVar, StringVar
from tkinter.ttk import Radiobutton, Button, Entry, Label

from ModeSelector import ModeSelector
def time_tracker(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f"A função {func.__name__} levou {end_time - start_time:.2f} segundos para ser executada.")
        return result
    return wrapper

# Função para escolher aleatoriamente uma fonte
def escolher_fonte():
    return choice(fontes)

# Função para escolher aleatoriamente uma palavra e criar uma janela com a fonte escolhida
def criar_janela():
    palavra = choice(palavras)
    fonte = escolher_fonte()
    janela = Tk()
    janela.geometry("600x400")
    janela.title("Identifique a fonte")
    label1 = Label(janela, text="Selecione o nome da fonte dentre as opções abaixo:")
    label1.pack(pady=20)
    label2 = Label(janela, text=palavra, font=(fonte, 48))
    label2.pack(pady=20)
    opcoes = []
    opcao_correta = escolher_opcao(fonte)
    for i in range(3):
        if i == opcao_correta:
            opcoes.append(fonte)
        else:
            opcao = escolher_fonte()
            while opcao == fonte or opcao in opcoes:
                opcao = escolher_fonte()
            opcoes.append(opcao)
    opcao1 = Button(janela, text=opcoes[0], command=lambda: verificar_fonte(opcoes[0], fonte, janela))
    opcao1.pack(pady=10)
    opcao2 = Button(janela, text=opcoes[1], command=lambda: verificar_fonte(opcoes[1], fonte, janela))
    opcao2.pack(pady=10)
    opcao3 = Button(janela, text=opcoes[2], command=lambda: verificar_fonte(opcoes[2], fonte, janela))
    opcao3.pack(pady=10)
    janela.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
    janela.mainloop()

# Função para escolher aleatoriamente a opção correta
def escolher_opcao(fonte):
    return random.randint(0, 2)

# Função para verificar se o nome da fonte escolhido está correto
def verificar_fonte(nome_fonte, fonte_correta, janela):
    if nome_fonte.lower() == fonte_correta.lower():
        print("Parabéns, você acertou!")
    else:
        print(f"Ops, você errou. A fonte correta era {fonte_correta}.")
    janela.destroy()

# Função principal que executa o jogo
def jogar():
    pontos = 0
    continuar_jogando = True
    while continuar_jogando:
        criar_janela()
        pontos += 1
        print(f"Você tem {pontos} ponto(s).\n")
        time.sleep(1)


