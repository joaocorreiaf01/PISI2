import random

LETRAS = "ABCDEFGHIJKLMNOPQSTUVWXYZ"  # sem o R, que é a origem


def ler_matriz(caminho):
    with open(caminho) as arquivo:
        linhas = [linha.split() for linha in arquivo if linha.strip()]
    return linhas[1:]


def encontrar_origem(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == "R":
                return (i, j)


def sortear_pontos(matriz, quantidade, gerador=random):
    ocupadas = [encontrar_origem(matriz)]
    pontos = {}
    colisoes = 0

    while len(pontos) < quantidade:
        i = gerador.randint(0, len(matriz) - 1)
        j = gerador.randint(0, len(matriz[0]) - 1)

        if (i, j) in ocupadas:
            colisoes += 1
        else:
            ocupadas.append((i, j))
            pontos[LETRAS[len(pontos)]] = (i, j)

    return pontos, colisoes
