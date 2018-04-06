"""
    Aluna: Caroline Jesuíno Nunes da Silva
    NUSP: 9293925
    SCC0251 - Processamento de Imagens
    2018/1
    Trabalho 3 - Filtragem 1D
"""
'''
    TODO:
    Filtro arbitrario espacial
'''



import numpy as np
import imageio


def unidimensionaliza(imagem, x, y):
    vetor = np.zeros(x*y)
    for i in range(x):
        for j in range(y):
            vetor[i*j + j] = imagem[i][j]

    return vetor


def arbitrarioespacial(vetor, x, y, pesos):



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

    if filtro == 1 && dominio == 1:
        imagem = arbitrarioespacial(unidimensional, x, y, pesos)



if __name__ == __main__:
    main()