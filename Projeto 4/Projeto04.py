"""
    Aluna: Caroline Jesuíno Nunes da Silva
    N USP: 929395
    Disciplina SCC0251 - Processamento de Imagens
    2018/1
    Trabalho 4 - Filtragem 2D
"""


import numpy as np
import imageio


def convolucao(imagem, filtro):
    xim, yim = imagem.shape()
    xf, yf, = filtro.shape()
    convoluida = np.zeros([xim - 2, yim - 2])
    filtroflip = np.flipud(np.fliplr(filtro))


    for i in range(1, xim - 1):
        for j in range(1, yim - 1):
            convoluida[i][j] = imagem[i - 1 : i + xf - 1, j - 1 : j + yf - 1] * filtroflip

    return convoluida


def operador_sobel(imagem):
    # define os filtros de sobel
    filtrox = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    filtroy = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    x, y = imagem.shape

    # cria imagem com as bordas zeradas para realizar a convolução
    # pode-se usar o indice dois porque o tamanho do filtro é fixo
    imagemborda = np.zeros([x + 2, y + 2])
    for i in range(1, x + 1):
        for j in range(1, y + 1):
            imagemborda[i, j] = imagem[i - 1, j - 1]

    # chama a convolução para os dois filtros diferentes
    imagemx = convolucao(imagemborda, filtrox)
    imagemy = convolucao(imagemborda, filtroy)

    # calcula a imagem resultante com base na fórmula descrita na especificação
    resultante = np.zeros([x, y])
    for i in range(x):
        for j in range(y):
            resultante[i][j] = np.sqrt((imagemx[i][j] ** 2) + (imagemy[i][j] ** 2))

    # aplica a transformada discreta de fourier em duas dimensões
    resultante = np.real(np.fft2(resultante))

    return resultante


def cortes(imagem, indicecortes):
    x, y = imagem.shape()

    corte1 = imagem[0:x/2, 0:y/2]
    x1, y1 = corte1.shape()
    indicecortes[0] *= y1
    indicecortes[1] *= y1
    indicecortes[2] *= x1
    indicecortes[3] *= x1

    corte2 = corte1[indicecortes[0]:indicecortes[1], indicecortes[2]:indicecortes[3]]
    return corte2


def unidimensionaliza(quadrante):
    x, y = quadrante.shape()
    ibagem = np.zeros(x*y)

    for i in range(x):
        for j in range(y):
            ibagem[(i*y) + j] = quadrante[i][j]

    return ibagem


def NN(quadrante, dataset, labels):
    ibagem = unidimensionaliza(quadrante)
    x, y = dataset.shape()
    minimo = np.dot(ibagem, dataset[0])
    indice = 0
    for i in range(1, y):
        resultado = np.dot(ibagem, dataset[i])
        if resultado < minimo:
            minimo = resultado
            indice = i

    return(labels[indice], indice)



def main ():
    # lendo os parametros de entrada
    nome_imagem = input()
    metodo = int(input())
    if metodo == 1:
        hfiltro = int(input())
        wfiltro = int(input())
        filtro = np.zeros([hfiltro, wfiltro])
        for i in range(hfiltro):
            linha = input()
            linha = linha.split()
            for j in range(wfiltro):
                filtro[i][j] = float(linha[j])
    elif metodo == 2:
        tamfiltro = int(input())
        sigma = float(input())
    c = input()
    c = c.split()
    nome_dataset = input()
    nome_labels = input()

    # carregando dados com base na entrada
    indicecortes = (float(c[1]), float(c[2]), float(c[3]), float(c[4]))
    imagem = imageio.imread(nome_imagem)
    dataset = np.load(nome_dataset)
    labels = np.load(nome_labels)

    if metodo == 1:
    elif metodo == 2:
    else:
        processada = operador_sobel(imagem)

    quadrante = cortes(processada, indicecortes)
    resultado = NN(quadrante, dataset, labels)

    print(resultado[0]\n resultado[1])

if __name__ == '__main__':
    main()