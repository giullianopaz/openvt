#! /usr/bin/python
# -*- coding: UTF-8 -*-

# Autor: Giulliano Paz
# E-mail: giulliano94@gmail.com

# Classe para troca de cores de fontes e fundos
# para uma melhor destaque em execuções de código

# Variável para deixar fonte em negrito
BOLD = '\33[1m'

DEFAULT = '\33[0;0m'

REVERSE = '\33[2m'

# Dicionário de cores para o texto
FONT = {
    #cores em inglês
    'black': '\33[30m',
    'red': '\33[31m',
    'green': '\33[32m',
    'yellow': '\33[33m',
    'blue': '\33[34m',
    'pink': '\33[35m',
    'cyan': '\33[36m',
    'white': '\33[37m',
    'REVERSE': '\33[2m',
    None: ''
}
# Dicionário de cores para fundo
BACKGROUND = {
    #cores em inglês
    'black': '\33[40m',
    'red': '\33[41m',
    'green': '\33[42m',
    'yellow': '\33[43m',
    'blue': '\33[44m',
    'pink': '\33[45m',
    'cyan': '\33[46m',
    'white': '\33[47m',
    'REVERSE': '\33[2m',
    None: ''
}

#################### Método para informar erro ######################
def error(arg):

    if arg == 'fontcolor': arg = 'Fonte'
    if arg == 'bgcolor': arg = 'Fundo'

    msg1 = "\n >> Cor não disponível para {}!".format(arg)
    msg2 = "\n\n >> Lista de cores: [black, red, green, yellow, blue, pink, cyan, white]\n\n"

    print("{}{}{}{}{}".format(BOLD, FONT['white'], BACKGROUND['red'], msg1, DEFAULT), end='')
    print("{}{}{}{}{}".format(BOLD, FONT['white'], BACKGROUND['red'], msg2, DEFAULT), end='')

def color(text=None, fontcolor=None, bgcolor=None, bold=False):
    # Verifica se fontcolor foi informada
    if fontcolor != None: fontcolor = fontcolor.rstrip("\n").strip("\n").rstrip(" ").strip(" ")
    # Verifica se fontcolor foi informada de forma correta
    if fontcolor not in FONT: error('fontcolor')

    # Verifica se bgcolor foi informado
    if bgcolor != None: bgcolor = bgcolor.rstrip("\n").strip("\n").rstrip(" ").strip(" ")
    # Verifica se bgcolor foi informado corretamente
    if bgcolor not in BACKGROUND: error('bgcolor')

    bold = BOLD if bold != False else ''
    if not isinstance(text, (str)): text = str(text)

    return "{}{}{}{}{}".format(bold, FONT[fontcolor], BACKGROUND[bgcolor], text, DEFAULT)

############## Método para imprimir texto e fundos colorido ############
def cprint(text=None, fontcolor=None, bgcolor=None, bold=False):

    # Verifica se fontcolor foi informada
    if fontcolor != None: fontcolor = fontcolor.rstrip("\n").strip("\n").rstrip(" ").strip(" ")
    # Verifica se fontcolor foi informada de forma correta
    if fontcolor not in FONT: error('fontcolor')

    # Verifica se bgcolor foi informado
    if bgcolor != None: bgcolor = bgcolor.rstrip("\n").strip("\n").rstrip(" ").strip(" ")
    # Verifica se bgcolor foi informado corretamente
    if bgcolor not in BACKGROUND: error('bgcolor')

    bold = BOLD if bold != False else ''
    if not isinstance(text, (str)): text = str(text)

    # Imprime na tela o texto passado por parâmetro com as cores especificadas também por parâmetro
    # A sequência é imprimir  <BOLD> <fontcolor> <bgcolor> <text> <DEFAULT>
    # <BOLD> deixa o texto em negrito, <fontcolor> muda a cor da fonte, <bgcolor> muda a cor do fundo
    # <text> é o texto informado pelo usuário e <DEFAULT> faz voltar para as configuraçõe de cores padrão(Para não ficar sempre colorido)
    print("{}{}{}{}{}".format(bold, FONT[fontcolor], BACKGROUND[bgcolor], text, DEFAULT), end='')