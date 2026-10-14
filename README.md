# FlyFood

Encontra a menor rota do drone usando **distância de Manhattan**, comparando duas abordagens:

```
flyfood-sem-otimizacao/ -> força bruta (testa todas as ordens possíveis dos pontos)
flyfood-otimizado/      -> algoritmo genético (em desenvolvimento)
```

Cada pasta é um projeto independente, com a mesma estrutura:

```
main.py              -> roda o programa
src/matriz/matriz.py -> ler a matriz, achar a origem (R) e sortear os pontos
src/rota/rota.py     -> distância de Manhattan, custo da rota e o algoritmo de busca
data/entrada/        -> matriz.txt (5x6, só com o R)
data/saida/          -> um log por execução (resultados)
```

## Como rodar

```bash
python3 flyfood-sem-otimizacao/main.py
python3 flyfood-otimizado/main.py
```

O programa gera rodadas sem parar: 2 pontos, 3 pontos, 4 pontos...
Em cada rodada os pontos são sorteados na matriz. Se o sorteio cair numa posição já ocupada,
conta como **colisão** e sorteia de novo. Para parar, aperte **Ctrl+C**.

Cada rodada é salva no log (`data/saida/` da pasta que foi executada) com a rota, o custo,
as colisões e o tempo. No início fica a seed do sorteio e, no final, o total de colisões.
