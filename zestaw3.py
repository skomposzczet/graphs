from graph import *
import networkx as nx
import random
import heapq

def convert_to_weighted(min: int, max: int, adjacency_list: dict) -> dict:
    weighted = {v: {} for v in adjacency_list}
    for u, neighbors in adjacency_list.items():
        weighted[u] = {}
        for v in neighbors:
            weight = random.randint(min, max)
            weighted[u][v] = weight
            weighted[v][u] = weight
    return weighted


def dijkstra(adjacency_list, start):
    # initialize the distances dictionary with infinite distances for all nodes except start node
    distances = {node: float('inf') for node in adjacency_list}
    distances[start] = 0
    
    # initialize the priority queue with the start node
    priority_queue = [(0, start)]
    
    # initialize the paths dictionary with empty paths for all nodes except start node
    paths = {node: [] for node in adjacency_list}
    paths[start] = [start]
    
    while priority_queue:
        # get the node with the smallest distances from the start node
        (current_distance, current_node) = heapq.heappop(priority_queue)
        
        # if the distances to the current node is greater than the smallest distances in the priority queue,
        # skip this node and move on to the next one
        if current_distance > distances[current_node]:
            continue
        
        # loop through the neighbors of the current node
        for neighbor, weight in adjacency_list[current_node].items():
            # calculate the distances to the neighbor node
            new_distance = distances[current_node] + weight
            
            # if the new distances is smaller than the current distances, update the distances and paths dictionaries
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current_node] + [neighbor]
                
                # add the neighbor to the priority queue with the new distances
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return adjacency_list.keys(), start, distances, paths

def pretty_print(nodes, start, distances, paths):
    print(f"START: s = {start}")
    for node in nodes:
        print("d({:<2d}) = {:<2d} ==> {}".format(int(node), int(distances[node]), paths[node]))


def distance_matrix(graph):
    number_of_nodes = len(graph)
    matrix = np.zeros((number_of_nodes, number_of_nodes), dtype=int)
    for i in range(number_of_nodes):
        _, _, distances, _ = dijkstra(graph, i+1)
        for j in range(number_of_nodes):
            matrix[i][j] = distances[j+1]
    return matrix


def minimax_center(matrix):
    max_distances = np.max(matrix, axis=1)
    index = np.argmin(max_distances)
    return index+1, max_distances[index]


def center_of_graph(matrix):
    sums = np.sum(matrix, axis=1)
    index = np.argmin(sums)
    return index+1, sums[index]


def kruskal(graph):
    # utworzenie zbiorów wierzchołków
    vertices = set()
    for v1, edges in graph.items():
        vertices.add(v1)
        vertices.update(edges.keys())
        
    # stworzenie zbiorów dla każdego wierzchołka
    sets = {}
    for v in vertices:
        sets[v] = {v}
        
    # utworzenie listy krawędzi
    edges = []
    for v1, edges_dict in graph.items():
        for v2, weight in edges_dict.items():
            edges.append((weight, v1, v2))
    
    # sortowanie krawędzi po wagach
    edges.sort()
    
    # lista krawędzi w drzewie rozpinającym
    mst = []
    
    for weight, v1, v2 in edges:
        if sets[v1] != sets[v2]:
            mst.append((v1, v2, weight))
            # połączenie zbiorów wierzchołków
            sets[v1] |= sets[v2]
            for v in sets[v2]:
                sets[v] = sets[v1]
            if len(sets[v1]) == len(vertices):
                break
                
    return mst

    

## Zad 1
while(True):
    graph = RandomGraph.random_np(12, 0.3)
    weighted = convert_to_weighted(1, 10, graph.as_adjacency_list())
    G = nx.Graph(weighted, weighted=True)
    if nx.is_connected(G):
        break


## Zad 2
nodes, start, distances, paths = dijkstra(weighted,1)
pretty_print(nodes, start, distances, paths)

## Zad3
matrix = distance_matrix(weighted)
print(matrix)

## Zad4
center, distance = center_of_graph(matrix)
print(f"Centrum grafu to {center} (suma odległości: {distance})")

center, distance = minimax_center(matrix)
print(f"Centrum minimax grafu to {center} (odległość od najdalszego: {distance})")

## Zad5
mst = kruskal(weighted)
print(mst)