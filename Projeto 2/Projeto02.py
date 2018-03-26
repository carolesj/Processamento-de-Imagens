"""
Aluna: Caroline Jesuíno Nunes da Silva
Número USP: 9293925
Disciplina SCC0251 - Processamento de Imagens
2018/1
Trabalho 2 - Realce e Superresolução
"""

import imageio
import numpy as np
import matplotlib as plt


def histograma_transf_individual(img1, img2, img3, img4):
    return


def histograma_transf_conjunta(img1, img2, img3, img4):
    return


def ajuste_gamma(img1, img2, img3, img4, gama):
    return


def superresolucao(img1, img2, img3, img4):
    return


def rmse(gerada, imghq):
    return


def main():
    nome_base = input()
    nome_hq = input()
    realce = int(input())
    gama = input()

    img1 = imageio.imread(nome_base + '1.png')
    img2 = imageio.imread(nome_base + '2.png')
    img3 = imageio.imread(nome_base + '3.png')
    img4 = imageio.imread(nome_base + '4.png')
    imghq = imageio.imread(nome_hq + '.png')

    if realce == 1:
        histograma_transf_individual(img1, img2, img3, img4)
    elif realce == 2:
        histograma_transf_conjunta(img1, img2, img3, img4)
    elif realce == 3:
        ajuste_gamma(img1, img2, img3, img4, gama)

    gerada = superresolucao(img1, img2, img3, img4)
    erro = rmse(gerada, imghq)

    print("%.4f" % erro)

if __name__ == '__main__':
    main()