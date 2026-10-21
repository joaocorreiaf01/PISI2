#funcao que retorna o custo total do caminho:
def custoCaminho(permutacao, dicDistancias):
    soma = 0
    for i in range(len(permutacao) - 1):
        soma += dicDistancias[(permutacao[i], permutacao[i + 1])]
    #soma também a volta do ultimo no pro primeiro
    soma += dicDistancias[(permutacao[-1], permutacao[0])]
    return soma


def aptidao(individuo, dicDistancias):
    #objetivo minimizar, entao quanto menor o custo, mais apto o individuo
    return custoCaminho(individuo, dicDistancias)


def calculaAptidao(populacao, dicDistancias):
    #obs: a posicao k da lista é a aptidao do individuo k da populacao
    return [aptidao(individuo, dicDistancias) for individuo in populacao]
