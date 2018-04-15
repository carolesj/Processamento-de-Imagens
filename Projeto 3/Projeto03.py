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
    meiop = int(np.floor(tamp/2))
    filtro = np.zeros(tamp)
    # garante que o vetor de pesos estará invertido na hora da multiplicação
    for i in range (tamp):
        filtro[i] = pesos[tamp - i - 1]
    for i in range(tamv):
        atual = 0
        # percorre do meio ao começo
        for j in range(i, i - meiop, -1):
            atual += vetor[j] * filtro[j-i+tamp-1]
        # percorre do meio ao fim
        for j in range(i + 1, i + meiop):
            atual += vetor[j%tamv] * filtro[(j-i+tamp)%tamp]
        processado[i] = atual / tamp
    return processado


# constroi o filtro gaussiano
def gaussiano(delta, tamf):
    filtro = np.zeros(tamf)
    centro = np.floor(tamf/2)
    membro1 = (1 / (np.sqrt(2*math.pi*delta)))
    divisor = 2*(delta**2)

    for i in range(tamf):
        if i < centro:
            filtro[i] = membro1 * (np.exp(((-i+centro)**2)/divisor))
        else:
            filtro[i] = membro1 * (np.exp(((i-centro)**2)/divisor))
    return filtro


# realiza a transformada discreta de fourier
def tdf(unidimensional, tamv):
    transformado = np.zeros(tamv, dtype=np.complex64)
    x = np.arange(tamv)

    for freq in np.arange(tamv):
        transformado[freq] = np.sum(np.multiply(unidimensional, np.exp((-1j*2*np.pi*freq*x)/freq)))

    return transformado


# realiza a transformada inversa de fourier
def tdfi(transformado, tamv):
    unidimensional = np.zeros(tamv, dtype=np.float32)
    freq = np.arange(tamv)

    for i in np.arange(tamv):
        unidimensional[i] = np.real(np.sum(np.multiply(transformado, np.exp((1j*2*np.pi*freq*i)/tamv))))

    return unidimensional/tamv


# realiza a convolução no domínio da frequência
def dominiofrequencia(vetor, tamv, pesos, tamp):
    dif = tamv - tamp
    difv = np.zeros(dif)
    pesos += difv

    vetort = tdf(vetor, tamv)
    pesost = tdf(pesos, tamp)

    resultado = np.multiply(vetort, pesost)
    resultado = tdfi(resultado, tamv)

    return np.real(resultado)


def ajustaimagem(vetor, x, y):
    imagem = np.zeros([x, y])
    maximo = np.max(vetor)
    minimo = np.min(vetor)

    for i in range(x):
        for j in range(y):
            imagem[i][j] = (((vetor[i*x+j] - minimo) / (maximo - minimo)) * 255)

    return imagem


def rmse(imagemprocessada, imagem, x, y):
    erro = 0
    for i in range(x):
        for j in range(y):
            erro += (imagem[i][j] - imagemprocessada[i][j])**2
    return np.sqrt((1/x*y) * erro)


def main():
    nomeimg = str(input()).rstrip()
    filtro = int(input())
    tamfiltro = int(input())
    if filtro == 1:
        pesos_string = input()
        pesos_string = pesos_string.split()
        pesos = np.zeros(tamfiltro)
        for i in range(tamfiltro):
            pesos[i] = float(pesos_string[i])
    else:
        delta = float(input())
    dominio = int(input())

    imagem = imageio.imread(nomeimg)
    x, y = imagem.shape
    unidimensional = unidimensionaliza(imagem, x, y)

    if filtro == 1 and dominio == 1:
        imagemr = arbitrarioespacial(unidimensional, x*y, pesos, tamfiltro)
    elif filtro == 2 and dominio == 1:
        filtro = gaussiano(delta, tamfiltro)
        imagemr = arbitrarioespacial(unidimensional, x*y, filtro, tamfiltro)
    elif filtro == 1 and dominio == 2:
        imagemr = dominiofrequencia(unidimensional, x*y, pesos, tamfiltro)
    else:
        filtro = gaussiano(delta, tamfiltro)
        imagemr = dominiofrequencia(unidimensional, x*y, filtro, tamfiltro)

    imagemprocessada = ajustaimagem(imagemr, x, y)
    erro = rmse(imagemprocessada, imagem, x, y)

    print("%.4f" % erro)


if __name__ == '__main__':
    main()