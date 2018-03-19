'''
Aluna: Caroline Jesuíno Nunes da Silva
Numero USP: 9293925
Disciplina: SCC0251
Ano/semestre: 2018/1
Trabalho 1 - Gerador de imagens
'''

'''
Todo:
    .random walk
    .normalizar as matrizes geradas
    .digitalização
    .comparação
'''
import numpy as np
import random as rand

def le_matriz(nome_arquivo) :
    #carrega uma imagem ao ler um nome de arquivo
    #e remover possíveis caracteres em branco
    img = np.load(nome_arquivo.rstrip())
    return img

#f(x,y) = (x + y)
def funcao1(tamC) :
    gerada = np.zeros((tamC, tamC))
    for i in range(tamC):
        for j in range(tamC):
            gerada[i][j] = i + j
    #matriz retornada com valores não normalizados
    return gerada

#f(x,y) = |sen(x/Q) + sen(y/Q)|
def funcao2(Q, tamC) :
    gerada = np.zeros((tamC, tamC))
    for i in range(tamC):
        for j in range(tamC):
            gerada[i][j] = np.absolute(np.sin(i/Q) + np.sin(j/Q))
    return gerada

#f(x,y) = [(x/Q) - sqrt(y/Q)]
def funcao3(Q, tamC) :
    gerada = np.zeros((tamC, tamC))
    for i in range(tamC):
        for j in range(tamC):
            gerada[i][j] = (i/Q - np.sqrt(j/Q))
    return gerada

#f(x,y) = rand(0, 1, S)
def funcao4(tamC, S) :
    rand.seed(S)
    gerada = np.zeros((tamC, tamC))
    for i in range(tamC):
        for j in range(tamC):
            gerada[i][j] = rand.random()
    return gerada

#f(x,y) = randomwalk(S)
#número de passos = 1 + (C^2)/2
def funcao5() :
    gerada = 0
    return gerada

#recebe a imagem gerada e a normaliza baseando-se no número
#de bits por pixel informados na entrada
def normalizaImagem(gerada, nbitspp) :
    normalizada = 0
    return normalizada

def main() :
    nome_arquivo = input()
    tamC = input()
    tipo = int(input())
    Q = input()
    tamN = input()
    nbitspp = input()
    S = input()

    carregada = le_matriz(nome_arquivo)

    if tipo == 1:
        gerada = funcao1(tamC)
    elif tipo == 2:
        gerada = funcao2(Q, tamC)
    elif tipo == 3:
        gerada = funcao3(Q, tamC)
    elif tipo == 4:
        gerada = funcao4(tamC, S)
    else:
        gerada = funcao5(carregada, tamC, Q, tamN, nbitspp, S)

main()