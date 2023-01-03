from dijkstra import DijkstraSPF, Graph
import topologia_data
import numpy as np

# topologia rede c239
combos = []
for a, y in topologia_data.c239_adjacent_list.items():
    for z in y:
        combos.append((a, z))
edge_weights = dict(zip(combos, topologia_data.c239_length))
graph = Graph(topologia_data.c239_adjacent_list, edge_weights)


def generate_paths(adjacency, graf, matrix=False):
    shortest_path = []
    if not matrix:
        for i in range(1, len(adjacency.keys()) + 1):
            for j in range(1, len(adjacency.keys()) + 1):
                dijkstra = DijkstraSPF(graf, i)
                shortest_path.append((dijkstra.get_path(j), dijkstra.get_distance(j)))

    else:
        for i, j in enumerate(matrix):
            for s, k in enumerate(j):
                if k != 0:
                    dijkstra = DijkstraSPF(graf, i + 1)
                    shortest_path.append((dijkstra.get_path(s + 1), dijkstra.get_distance(s + 1)))

    shortest_path.sort(key=lambda var: (var[1], len(var[0])))

    aux = [b for b in shortest_path if b[1] != 0]

    for j in aux:
        s = j[0][0]
        d = j[0][-1]
        for i in aux:
            if i[0][0] == d and i[0][-1] == s:
                aux.remove(i)
    return aux


shortest_path_list = generate_paths(topologia_data.c239_adjacent_list, graph)


def deconstruct(paths):
    out = []
    for j in range(len(paths) - 1):
        out.append([paths[j], paths[j + 1]])
    return out


def flipped(key):
    for i in shortest_path_list:
        if list(key) in i:
            return key
    return key[::-1]


# ----------------------------------------------------------------------#


def first_fit(array):
    paths = []
    dicti = dict()
    og_dicti = dict()

    def first_missing(arrays):
        for g in range(1, 100):
            if g not in arrays:
                return g

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

    print("This is the First-Fit: ", og_dicti)


# ----------------------------------------------------------------------#


def most_used(array):
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
            mostuse = used(lambdas)
            dicti[flipped(tuple(i))].append(mostuse)
        lambdas.clear()
        og_dict[tuple(path)].append(mostuse)

    print("This is the Most Used: ", og_dict)


# ----------------------------------------------------------------------#


def random(array):
    paths = []
    dicti = dict()
    og_dict = dict()
    aux = []

    def assing(lambdas):
        for i in range(1, 100):
            aux.append(i)
        for _ in aux:
            random_wave = np.random.choice(aux, size=1)
            wave_length = random_wave[0]

            if wave_length not in lambdas:
                aux.clear()
                return wave_length
            else:
                aux.remove(wave_length)

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
            ran = assing(lambdas)
            dicti[flipped(tuple(i))].append(ran)
        lambdas.clear()
        og_dict[tuple(path)].append(ran)

    print("This is the Random:    ", og_dict)


first_fit(shortest_path_list)
most_used(shortest_path_list)
random(shortest_path_list)
