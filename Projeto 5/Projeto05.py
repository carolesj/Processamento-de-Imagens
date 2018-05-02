"""
    Aluna: Caroline Jesuíno Nunes da Silva
    NUSP: 9293925
    SCC 0512 - Processamento de Imagens
    2018/1
    Trabalho 5 - inpainting usando FFTs
"""


import numpy as np
import imageio


'Verifica quais valores da matriz estão com valores acima de 90% do ' \
'máximo do filtro ou abaixo de 1% do mínimo da imagem'
def filtraimagem(g, filtro):
    limitef = (np.max(filtro) * 0.9)
    limiteg = (np.max(g) * 0.01)

    np.where(g >= limitef, g, 0)
    np.where(g <= limiteg, g, 0)

    #print("Filtrada\n")
    return g


'Faz uma convolução com filtro de média para suavização da imagem'
def passamedia(g):
    x, y = g.shape
    temp = np.zeros(g.shape)
    for i in range(x):
        for j in range(y):
            temp[i][j] = np.real((np.sum(np.sum(g[i - 3 : ((i + 4) % x), j - 3 : ((j + 4) % y)])))/49)

    g = np.copy(temp)
    #print("Média passada\n")
    return g


'Normaliza os valores obtidos para que fiquem entre 0 e 255'
def normaliza(g):
    maximo = np.max(g)
    minimo = np.min(g)

    g = (((maximo - g) / (maximo - minimo)) * 255)

    #print("Normalizada\n")
    return np.real(g).astype(np.uint8)


'Aplica o filtro de GErchberg PApoulis, num momento de muito bom humor' \
'para programar, apelidado de gepeto para ser mais facilmente chamado'
def gepeto(imgi, imgm, T):
    filtro = np.fft.fft(imgm)

    #print(T)
    # para cada iteração solicitada
    for i in range(T):
        # passa a fourier e filtra a imagem, voltando-a pro domínio do espaço depois
        g = np.fft.fft(imgi)
        filtraimagem(g, filtro)
        g = np.fft.ifft(g)
        # convolui com um filtro de média
        g = passamedia(g)
        # normaliza o valor obtido
        g = normaliza(g)

        g = imgi * (1 - imgm / 255) + g * (imgm / 255)

    #print("Gepetado\n")
    return g



def rmse(imgo, imgr):
    #print("Entrou no erro")
    erro = 0
    x, y = imgr.shape

    for i in range(x):
        for j in range(y):
            erro += (imgo[i][j] - imgr[i][j]) ** 2

    erro = np.sqrt((1 / (x * y)) * erro)

    #print("Erro gerado\n")
    return erro


def main():
    imgo_n = input().rstrip()
    imgi_n = input().rstrip()
    imgm_n = input().rstrip()
    T = int(input())

    imgo = imageio.imread(imgo_n)
    imgi = imageio.imread(imgi_n)
    imgm = imageio.imread(imgm_n)

    imgr = gepeto(imgi, imgm, T)
    erro = rmse(imgo, imgr)

    print(erro)


if __name__ == '__main__':
    main()