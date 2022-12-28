import random
import numpy as np

from dijkstra import DijkstraSPF, Graph
import data
import tabelas

# cria o dicionário para o dijkstra com base nos caminhos e nas ligações

'''
combs = []
for a, y in data.t1_adjacency_list.items():
    for z in y:
        combs.append((a, z))
edge_weights = dict(zip(combs, data.t1_length))
print(edge_weights)
graph = Graph(data.t1_adjacency_list, edge_weights)
'''

combs = []
for a, y in data.c239_adjacency_list.items():
    for z in y:
        combs.append((a, z))

edge_weights = dict(zip(combs, data.c239_length))

graph = Graph(data.c239_adjacency_list, edge_weights)


# encontra os caminhos mais curtos para qq nos (não tem matriz de trafego)


def get_paths(adjacency, graf, matrix=False):
    """
    Com base no grafo e numa matrix de trafego que pode ser omitida, gera todos os caminhos possiveis entre os nós.
    Ordenado pelos caminhos mais curtos primeiro.
    Remove ainda entradas duplicadas, isto é licação 2->5 é igual a ligação 5->2. Remove a ultima.
    :param adjacency: (dict) um dicionario com key: nó; value: lista com as suas ligações
    :param graf: (Objeto Graph) objeto graph do dijkstra
    :param matrix: (lista de listas) matrix de trafego, pode ser omitida caso nao exista
    :return spf (list): uma lista com todos os caminhos e a sua distancia,
            ordenados por ordem crscente de distancia e numero de saltos
    """

    spf = []
    if not matrix:
        for i in range(1, len(adjacency.keys()) + 1):
            for j in range(1, len(adjacency.keys()) + 1):
                dijkstra = DijkstraSPF(graf, i)
                spf.append((dijkstra.get_path(j), dijkstra.get_distance(j)))

        # encontra os caminhos mais curtos para qq nos com base na matrix de tráfego

    else:
        for i, j in enumerate(matrix):
            print(i, j)
            for s, k in enumerate(j):  # enumera os valores da linha da matriz
                if k != 0:
                    dijkstra = DijkstraSPF(graf, i + 1)
                    spf.append((dijkstra.get_path(s + 1), dijkstra.get_distance(s + 1)))

    # shortest path first (ordena por distancia, em caso de empate pelo numero de nós -- menos nos aparecem primeiro)
    spf.sort(key=lambda var: (var[1], len(var[0])))

    # remove as duplicadas pk esta lib de dijsktra é unidirecional precisamos de meter os dois caminhos ex. (1,2) e (2,1)
    # pode dar problemas se o dijkstra nao der o mesmo caminho para 25 e 52 (deve estar resolvido)

    plh = [b for b in spf if b[1] != 0]

    for j in plh:
        s = j[0][0]
        d = j[0][-1]
        for i in plh:
            if i[0][0] == d and i[0][-1] == s:
                plh.remove(i)
    return plh


# spf_list = get_paths(data.t1_adjacency_list, graph, data.t1_traffic_matrix)

spf_list = get_paths(data.c239_adjacency_list, graph)


# print(spf_list)
# tabelas.tabelas(spf_list, ["path", "km"])


# tabelas.tabelas(data.t1_traffic_matrix, [i for i in range(1, 7)], [i for i in range(1, 7)])


# fazer lambdas e nao copiar do rodrigo
def deconstruct(paths):
    out = []
    for j in range(len(paths) - 1):
        out.append([paths[j], paths[j + 1]])
    return out


def first_fit(array):
    paths = []
    dicti = dict()
    og_dicti = dict()

    def first_missing(arrays):
        for g in range(1, 100):
            if g not in arrays:
                return g

    def flipped(key):
        for i in spf_list:
            if list(key) in i:
                return key
        return key[::-1]

    # dicionário
    for i in array:
        paths.append(tuple(i[0]))

    for path in paths:
        og_dicti[tuple(path)] = []
        for i in deconstruct(path):
            if (tuple(i) not in dicti.keys()) and (tuple(i)[::-1] not in dicti.keys()):
                dicti[tuple(i)] = []

    for path in paths:
        lambdas = []
        for i in deconstruct(path):
            for l in dicti[flipped(tuple(i))]:
                lambdas.append(l)
            ff = first_missing(lambdas)
            dicti[flipped(tuple(i))].append(ff)
        og_dicti[tuple(path)].append(ff)
        lambdas.clear()

    print("This is the GOAT: ", og_dicti)


# ----------------------------------------------------------------------#

def most_used2(array):
    paths = []
    dicti = dict()
    og_dict = dict()
    lamda_dict = dict()
    for g in range(1, 100):
        lamda_dict[g] = 0

    def used(lambdas):
        for i in sorted(lamda_dict, key=lamda_dict.get, reverse=True):
            if i not in lambdas:
                var = lamda_dict[i]
                var = var + 1
                lamda_dict[i] = var
                return i

    def flipped(key):
        for i in spf_list:
            if list(key) in i:
                return key
        return key[::-1]

    # dicionário
    for i in array:
        paths.append(tuple(i[0]))

    for path in paths:
        og_dict[tuple(path)] = []
        for i in deconstruct(path):
            if (tuple(i) not in dicti.keys()) and (tuple(i)[::-1] not in dicti.keys()):
                dicti[tuple(i)] = []

    for path in paths:
        lambdas = []
        for i in deconstruct(path):
            for l in dicti[flipped(tuple(i))]:
                lambdas.append(l)
            ff = used(lambdas)
            dicti[flipped(tuple(i))].append(ff)
        lambdas.clear()
        og_dict[tuple(path)].append(ff)

    print("This is the Lambdas: ", og_dict)


def random(array):
    paths = []
    dicti = dict()
    og_dict = dict()
    aux = []

    def assing(lambdas):
        for i in range(1, 100):
            aux.append(i)
        for j in aux:
            random_wave = np.random.choice(aux, size=1)
            wave_lenght = random_wave[0]

            if wave_lenght not in lambdas:
                aux.clear()
                return wave_lenght
            else:
                aux.remove(wave_lenght)

    def flipped(key):
        for i in spf_list:
            if list(key) in i:
                return key
        return key[::-1]

    # dicionário
    for i in array:
        paths.append(tuple(i[0]))

    for path in paths:
        og_dict[tuple(path)] = []
        for i in deconstruct(path):
            if (tuple(i) not in dicti.keys()) and (tuple(i)[::-1] not in dicti.keys()):
                dicti[tuple(i)] = []

    for path in paths:
        lambdas = []
        for i in deconstruct(path):
            for l in dicti[flipped(tuple(i))]:
                lambdas.append(l)
            ff = assing(lambdas)
            dicti[flipped(tuple(i))].append(ff)
        lambdas.clear()
        og_dict[tuple(path)].append(ff)

    print("This is the Random: ", og_dict)


first_fit(spf_list)
most_used2(spf_list)
random(spf_list)
