from itertools import permutations


def distancia(a, b):
    # Distância de Manhattan: o drone só anda na horizontal e na vertical
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def custo_da_rota(rota, origem, pontos):
    custo = 0
    atual = origem
    for letra in rota:
        custo += distancia(atual, pontos[letra])
        atual = pontos[letra]
    custo += distancia(atual, origem)  # volta para o R
    return custo


def forca_bruta(origem, pontos):
    # Testa todas as ordens possíveis (n!) e fica com a de menor custo
    melhor_rota = None
    menor_custo = None

    for rota in permutations(pontos):
        custo = custo_da_rota(rota, origem, pontos)
        if menor_custo is None or custo < menor_custo:
            menor_custo = custo
            melhor_rota = rota

    return melhor_rota, menor_custo
