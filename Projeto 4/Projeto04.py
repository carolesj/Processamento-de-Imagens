"""
    Aluna: Caroline Jesuíno Nunes da Silva
    N USP: 929395
    Disciplina SCC0251 - Processamento de Imagens
    2018/1
    Trabalho 4 - Filtragem 2D
"""


import numpy as np
import imageio


def filtragem(imagem, filtro):
    filtroexpandido = np.zeros(imagem.shape)
    resultante = np.zeros(imagem.shape)
    for i in range(filtro.shape[0]):
        for j in range(filtro.shape[1]):
            filtroexpandido[i][j] = filtro[i][j]
    filtroexpandido = np.fft.fft2(filtroexpandido)
    resultante = np.fft.fft2(imagem)
    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            resultante[i][j] *= filtroexpandido[i][j]

    return resultante



# apenas aplica a formula para achar o filtro
def _laplaciana_gaussiana(inicio, fim, sigma):
    # os membros foram separados para visualização mais simples
    membro1 = -(1 / np.pi * (sigma**4))
    membro2 = 1-(inicio**2 + fim**2) / (2*(sigma ** 2))
    membro3 = np.exp(-((inicio**2 + fim**2) / 2 * (sigma**2)))

    return membro1 * membro2 * membro3


def normalizalg(filtro, tamfiltro):
    negativos, positivos = 0, 0
    for i in range(tamfiltro):
        for j in range(tamfiltro):
            if filtro[i][j] < 0:
                negativos += filtro[i][j]
            else:
                positivos += filtro[i][j]
    for i in range(tamfiltro):
        for j in range(tamfiltro):
            if filtro[i][j] < 0:
                filtro[i][j] *= (-positivos/negativos)
    return


def laplaciana_gaussiana(tamfiltro, sigma):
    filtro = np.zeros([tamfiltro, tamfiltro])
    # acha qual deve ser o valor de distância entre uma posição e outra
    # pra que elas sejam uniformemente distribuidas
    if tamfiltro % 2 == 0:
        passo = 10 / 2 * (tamfiltro - 1)
    else:
        passo = 10 / (tamfiltro - 1)

    #preenche o filtro utilizando a função descrita na especificação
    for i in range(tamfiltro):
        for j in range(tamfiltro):
            filtro[i][j] = _laplaciana_gaussiana((-5 + i*passo), (-5 + j*passo), sigma)

    normalizalg(filtro, tamfiltro)
    return filtro



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
    resultante = np.fft2(resultante)

    return resultante


def cortes(imagem, indicecortes):
    x, y = imagem.shape
    x, y = int(x/2), int(y/2)
    corte1 = imagem[0:x, 0:y]
    x1, y1 = corte1.shape
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
    indicecortes = (float(c[0]), float(c[1]), float(c[2]), float(c[3]))
    imagem = imageio.imread(nome_imagem)
    dataset = np.load(nome_dataset)
    labels = np.load(nome_labels)

    if metodo == 1:
        processada = filtragem(imagem, filtro)
    elif metodo == 2:
        filtro = laplaciana_gaussiana(tamfiltro, sigma)
        processada = filtragem(imagem, filtro)
    else:
        processada = operador_sobel(imagem)

    quadrante = cortes(processada, indicecortes)
    resultado = NN(quadrante, dataset, labels)

    print(resultado[0] + "\n" + resultado[1])

if __name__ == '__main__':
    main()