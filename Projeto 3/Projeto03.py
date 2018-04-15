"""
    Aluna: Caroline Jesuíno Nunes da Silva
    NUSP: 9293925
    SCC0251 - Processamento de Imagens
    2018/1
    Trabalho 3 - Filtragem 1D
"""
'''
    TODO:
'''



import numpy as np
import imageio
import math


# transforma uma imagem distribuida em linhas e colunas num vetor de uma linha
def unidimensionaliza(imagem, x, y):
    vetor = np.zeros(x*y)
    for i in range(x):
        for j in range(y):
            vetor[i*j + j] = imagem[i][j]

    return vetor


# realiza a filtragem arbitraria no dominio espacial
def arbitrarioespacial(vetor, tamv, pesos, tamp):
    processado = np.zeros(tamv)
    # ao fazer o floor, não importa se o tamanho do vetor é par ou impar
    meiop = np.floor(tamp/2)
    # garante que o vetor de pesos estará invertido na hora da multiplicação
    filtro = np.fliplr(pesos)
    for i in range(tamv):
        atual = 0
        # percorre do meio ao começo
        for j in range(i, i - meiop, -1):
            atual += vetor[j] * filtro[j-i+tamp]
        # percorre do meio ao fim
        for j in range(i + 1, i + meiop):
            atual += vetor[j%tamv] * filtro[j-i+tamp]
        processado[i] = atual / tamp
    return processado


# realiza o filtro gaussiano no domínio espacial
def gaussianoespacial(vetor, tamv, delta, tamf):
    processado = np.zeros(tamv)
    centro = np.floor(tamf/2)
    membro1 = 1 / (np.sqrt(2*math.pi*delta))

    for i in range(tamv):
        atual = 0
        for j in range(i + centro - 1, i, -1):
            atual += membro1 * np.exp(-((vetor[j] * -(j-i+centro))**2)/2*(delta**2))
        for j in range(i + centro, i + tamf, 1):
            atual += membro1 * np.exp(-((vetor[j%tamv] * (j-i+centro))**2)/2*(delta ** 2))
        processado[i] = atual/tamf
    return processado


def tdf():


def main():
    nomeimg = str(input()).rstrip()
    filtro = int(input())
    tamfiltro = int(input())
    if filtro == 1:
        pesos = np.zeros(tamfiltro)
        for i in range(tamfiltro):
            pesos[i] = float(input())
    else:
        delta = float(input())
    dominio = int(input())

    imagem = imageio.imread(nomeimg)
    x, y = imagem.shape
    unidimensional = unidimensionaliza(imagem, x, y)

    if filtro == 1 and dominio == 1:
        imagem = arbitrarioespacial(unidimensional, x*y, pesos, tamfiltro)
    elif filtro == 2 and dominio == 1:
        imagem = gaussianoespacial(unidimensional, x*y, delta, tamfiltro)



if __name__ == __main__:
    main()