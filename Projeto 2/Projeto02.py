"""
    Aluna: Caroline Jesuíno Nunes da Silva
    Número USP: 9293925
    Disciplina SCC0251 - Processamento de Imagens
    2018/1
    Trabalho 2 - Realce e Superresolução
"""


import imageio
import numpy as np
# import matplotlib.pyplot as plt


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
def equaliza_histograma_individual(img1, img2, img3, img4):
    equalizada1 = _equaliza_histograma_individual(img1)
    equalizada2 = _equaliza_histograma_individual(img2)
    equalizada3 = _equaliza_histograma_individual(img3)
    equalizada4 = _equaliza_histograma_individual(img4)

    return equalizada1, equalizada2, equalizada3, equalizada4


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

    return equalizada1, equalizada2, equalizada3, equalizada4


# percorre toda a imagem e aplica pixel a pixel a fórmula do ajuste
# gama baseada no expoente dado como entrada
def _ajuste_gama(img, expoente):
    ajustada = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            ajustada[i][j] = np.floor(((img[i][j]/255)**expoente) * 255)

    return img


# chama o ajuste gama par cada uma das imagens
def ajuste_gamma(img1, img2, img3, img4, gama):
    expoente = 1 / gama
    img1processada = _ajuste_gama(img1, expoente)
    img2processada = _ajuste_gama(img2, expoente)
    img3processada = _ajuste_gama(img3, expoente)
    img4processada = _ajuste_gama(img4, expoente)

    return img1processada, img2processada, img3processada, img4processada


def superresolucao(processadas):
    x, y = processadas[0].shape
    # o lado da imagem gerada será o dobro do lado das imagens base
    # porque para cada pixel original haverá 4
    acrescimo_lateral = 2
    xsr = x * acrescimo_lateral
    ysr = y * acrescimo_lateral
    gerada = np.zeros([xsr, ysr])
    # recupera cada imagem das tuplas retornadas
    img1 = processadas[0]
    img2 = processadas[1]
    img3 = processadas[2]
    img4 = processadas[3]

    # posiciona os pixels retirados das imagens originais da seguinte forma
    # em cada quadrante da imagem da superresolução
    # [[img1, img3],
    #   [img2, img4]]
    for i in range(0, xsr, 2):
        for j in range(0, ysr, 2):
            gerada[i][j] = (img1[int(np.floor(i/2))][int(np.floor(j/2))]).astype(np.uint8)
            gerada[i][j + 1] = (img2[int(np.floor(i/2))][int(np.floor(j/2))]).astype(np.uint8)
            gerada[i + 1][j] = (img3[int(np.floor(i/2))][int(np.floor(j/2))]).astype(np.uint8)
            gerada[i + 1][j + 1] = (img4[int(np.floor(i/2))][int(np.floor(j/2))]).astype(np.uint8)

    return gerada


def rmse(gerada, imghq):
    x, y = imghq.shape
    erro = 0

    for i in range(x):
        for j in range(y):
            erro += (imghq[i][j] - gerada[i][j]) ** 2
    erro = np.sqrt(erro) * (1/(x*y))

    return erro


def main():
    nome_base = str(input()).rstrip()
    nome_hq = str(input()).rstrip()
    realce = int(input())
    gama = float(input())

    img1 = imageio.imread(nome_base + '1.png')
    img2 = imageio.imread(nome_base + '2.png')
    img3 = imageio.imread(nome_base + '3.png')
    img4 = imageio.imread(nome_base + '4.png')
    imghq = imageio.imread(nome_hq + '.png')

    if realce == 1:
        processadas = equaliza_histograma_individual(img1, img2, img3, img4)
    elif realce == 2:
        processadas = equaliza_histograma_conjunto(img1, img2, img3, img4)
    elif realce == 3:
        processadas = ajuste_gamma(img1, img2, img3, img4, gama)
    else:
        processadas = (img1, img2, img3, img4)

    gerada = superresolucao(processadas)
    erro = rmse(gerada, imghq)

    print("%.4f" % erro)

    '''
    plt.title("Teste de Rorschach")
    plt.imshow(gerada, cmap='gray')
    plt.axis('off')
    plt.show()
    '''

if __name__ == '__main__':
    main()

