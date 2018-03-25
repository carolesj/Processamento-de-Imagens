"""
Aluna: Caroline Jesuíno Nunes da Silva
Numero USP: 9293925
Disciplina: SCC0251
Ano/semestre: 2018/1
Trabalho 1 - Gerador de imagens
"""


import numpy as np
import random as rand


def le_matriz(nome_arquivo):
    # carrega uma imagem ao ler um nome de arquivo
    # e remover possíveis caracteres em branco
    img = np.load(nome_arquivo.rstrip())
    return img


# f(x,y) = (x + y)
def funcao1(tamc):
    gerada = np.zeros((tamc, tamc))
    for i in range(tamc):
        for j in range(tamc):
            gerada[i][j] = i + j
    # matriz retornada com valores não normalizados
    return gerada


# f(x,y) = |sen(x/Q) + sen(y/Q)|
def funcao2(q, tamc):
    gerada = np.zeros((tamc, tamc))
    for i in range(tamc):
        for j in range(tamc):
            gerada[i][j] = np.absolute(np.sin(i/q) + np.sin(j/q))
    return gerada


# f(x,y) = [(x/Q) - sqrt(y/Q)]
def funcao3(q, tamc):
    gerada = np.zeros((tamc, tamc))
    for i in range(tamc):
        for j in range(tamc):
            gerada[i][j] = (i/q - np.sqrt(j/q))
    return gerada


# f(x,y) = rand(0, 1, S)
def funcao4(tamc, s):
    rand.seed(s)
    gerada = np.zeros((tamc, tamc))
    for i in range(tamc):
        for j in range(tamc):
            gerada[i][j] = rand.random()
    return gerada


# f(x,y) = randomwalk(S)
# número de passos = 1 + (C^2)/2
def funcao5(tamc, s):
    i = 0
    j = 0
    rand.seed(s)
    gerada = np.zeros((tamc, tamc))
    for n in range(1 + (tamc**2)/2):
        gerada[i][j] = 1
        i += rand.randrange(-1, 2, 1)
        j += rand.randrange(-1, 2, 1)
        i = divmod(i, tamc)
        j = divmod(j, tamc)

    return gerada


# recebe a imagem gerada e a normaliza baseando-se no número
# de bits por pixel informados na entrada
def normaliza_imagem(tamc, gerada):
    maximo = np.amax(gerada)
    limite = 65535
    for i in range(tamc):
        for j in range(tamc):
            gerada[i][j] = (gerada[i][j] / maximo) * limite
    return gerada


def digitaliza(normalizada, tamc, tamn, nbitspp):
    digitalizada = np.zeros((tamn, tamn))
    lado_matriz = int(tamc / tamn)
    maximo = 65535
    for i in range(tamn):
        for j in range(tamn):
            inicio_m = int(i * lado_matriz)
            fim_m = inicio_m + lado_matriz
            inicio_n = int(j * lado_matriz)
            fim_n = inicio_n + lado_matriz
            digitalizada[i][j] = np.amax(normalizada[inicio_m:fim_m,inicio_n:fim_n])
            digitalizada[i][j] = digitalizada[i][j] * (2**nbitspp) / maximo
    return digitalizada


def compara(lida, digitalizada, tamn):
    erro = 0
    for i in range(tamn):
        for j in range(tamn):
            erro = erro + ((digitalizada[i][j] - lida[i][j]) ** 2)
    erro = np.sqrt(erro)

    return erro


def main():
    nome_arquivo = input()
    tamc = int(input())
    tipo = int(input())
    q = int(input())
    tamn = int(input())
    nbitspp = int(input())
    s = int(input())

    carregada = le_matriz(nome_arquivo)

    if tipo == 1:
        gerada = funcao1(tamc)
    elif tipo == 2:
        gerada = funcao2(q, tamc)
    elif tipo == 3:
        gerada = funcao3(q, tamc)
    elif tipo == 4:
        gerada = funcao4(tamc, s)
    else:
        gerada = funcao5(tamc, s)

    normalizada = normaliza_imagem(tamc, gerada)
    digitalizada = digitaliza(normalizada, tamc, tamn, nbitspp)
    erro = compara(carregada, digitalizada, tamn)

    print("%.4f" % erro)


if __name__ == '__main__':
    main()