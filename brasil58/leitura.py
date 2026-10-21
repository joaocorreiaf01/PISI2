def lerDistancias(caminhoArquivo):
    #a matriz eh triangular superior, entao a linha i so tem os pesos de (i, i+1) pra frente
    distancias = {}
    with open(caminhoArquivo) as arquivo:
        for i, linha in enumerate(arquivo, start=1):
            for j, peso in enumerate(linha.split(), start=i + 1):
                #as arestas sao bidirecionais, entao grava em (i, j) e (j, i) com o mesmo peso
                distancias[(i, j)] = int(peso)
                distancias[(j, i)] = int(peso)
    return distancias
