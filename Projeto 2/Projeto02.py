"""
    Aluna: Caroline Jesuíno Nunes da Silva
    Número USP: 9293925
    Disciplina SCC0251 - Processamento de Imagens
    2018/1
    Trabalho 2 - Realce e Superresolução
"""
'''
    TO DO:
        Ajuste gama
        Superresolução
        Cálculo do erro
'''



import imageio
import numpy as np
import matplotlib as plt


# calcula o histograma para uma imagem individualmente
def calcula_histograma_individual(img):
    histograma = np.zeros([256])
    x, y = img.shape
    for i in range(x):
        for j in range(y):
            # acessa o vetor que representa o histograma na posição
            # descrita pelo valor de cada pixel da imagem e incrementa
            # a contagem daquele valor
            histograma[img[i][j]] += 1
    return histograma


# calcula o histograma para as quatro imagens ao mesmo tempo
# chamando a função de histograma individual e acumulando os
# resultados todos no mesmo vetor
def calcula_histograma_conjunto(img1, img2, img3, img4):
    histograma = calcula_histograma_individual(img1)
    histograma = np.add(histograma, calcula_histograma_individual(img2))
    histograma = np.add(histograma, calcula_histograma_individual(img3))
    histograma = np.add(histograma, calcula_histograma_individual(img4))
    return histograma


def _equaliza_histograma_individual(img):
    histograma = calcula_histograma_individual(img)
    # cria um histograma cumulativo no qual cada posição representa
    # o número de pixels existentes até aquele determinado tom de cinza
    histogramac = np.zeros(histograma.shape)
    histogramac[0] = histograma[0]
    tamanhoh = histograma.shape[0]
    x, y = img.shape

    # resolve as acumulações
    for i in range(1, tamanhoh):
        histogramac[i] = histograma[i] + histogramac[i - 1]

    # cria uma matriz do tamanho da imagem original para ser a
    # resultante, com valores inteiros de 8 bits
    equalizada = np.zeros(img.shape).astype(np.uint8)

    # aplica a formula da equalização para cada valor e atribui o
    # valor obtido para os correspondentes da posição do valor original
    for i in range(tamanhoh):
        valor_eq = ((tamanhoh - 1) / float(x * y)) * histogramac[i]
        equalizada[np.where(img == i)] = valor_eq

    return equalizada


# equaliza cada imagem individualmente e retorna os resuldados
def equalizacao_histograma_individual(img1, img2, img3, img4):
    equalizada1 = _equaliza_histograma_individual(img1)
    equalizada2 = _equaliza_histograma_individual(img2)
    equalizada3 = _equaliza_histograma_individual(img3)
    equalizada4 = _equaliza_histograma_individual(img4)

    return (equalizada1, equalizada2, equalizada3, equalizada4)


def equaliza_histograma_conjunto(img1, img2, img3, img4):
    # calcula o histograma conjunto e constroi o histograma cumulativo conjunto
    histograma = calcula_histograma_conjunto(img1, img2, img3, img4)
    histogramac = np.zeros(histograma.shape)
    histogramac[0] = histograma[0]
    tamanhoh = histograma.shape[0]
    x, y = img1.shape

    for i in range(1, tamanhoh):
        histogramac[i] = histograma[i] + histogramac[i - 1]

    # cria uma matriz para cada imagem equalizada
    equalizada1 = np.zeros(img1.shape).astype(np.uint8)
    equalizada2 = np.zeros(img1.shape).astype(np.uint8)
    equalizada3 = np.zeros(img1.shape).astype(np.uint8)
    equalizada4 = np.zeros(img1.shape).astype(np.uint8)

    # em cada matriz nova, na posição onde na matriz original havia o
    # valor descrito pela iteração, é posicionado o valor equalizado
    for i in range(tamanhoh):
        valor_eq = ((tamanhoh - 1) / float(x * y)) * histogramac[i]
        equalizada1[np.where(img1 == i)] = valor_eq
        equalizada2[np.where(img2 == i)] = valor_eq
        equalizada3[np.where(img3 == i)] = valor_eq
        equalizada4[np.where(img4 == i)] = valor_eq

    return (equalizada1, equalizada2, equalizada3, equalizada4)


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
        equalizacao_histograma_individual(img1, img2, img3, img4)
    elif realce == 2:
        equalizacao_histograma_conjunto(img1, img2, img3, img4)
    elif realce == 3:
        ajuste_gamma(img1, img2, img3, img4, gama)

    gerada = superresolucao(img1, img2, img3, img4)
    erro = rmse(gerada, imghq)

    print("%.4f" % erro)

if __name__ == '__main__':
    main()