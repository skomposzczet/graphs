from __future__ import annotations
from graph import _get_lines, BadGraphInput
from operator import itemgetter

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
from itertools import combinations
import random
import sys
def relax(vertices, edges, source):
    distances = {vertex: sys.maxsize for vertex in vertices}
    distances[source] = 0

    for _ in range(len(vertices) - 1):
        for start, end, weight in edges:
            if distances[start] + weight < distances[end]:
                distances[end] = distances[start] + weight

    return distances

class DiGraph:

    def __init__(self, n=0):
        self.matrix = np.zeros((n, n)).astype(int)
        self.weight = None

    def from_neighbourhood_matrix_file(self, filename: str):
        input = _get_lines(filename)
        self.from_neighbourhood_matrix(
            [[int(val) for val in line.split(' ')] for line in input])
        return self

    def from_neighbourhood_matrix(self, matrix: list):
        self.matrix = np.array(matrix)
        self.validate()
        return self

    def validate(self):
        if any([self.matrix[i][i] for i in range(len(self.matrix))]):
            self.matrix = None
            raise BadGraphInput("can't have loops")
        if any([v > 1 for row in self.matrix for v in row], ):
            self.matrix = None
            raise BadGraphInput("can't have multiple edges")
        return self

    def rand_wages(self, min_w=-5, max_w=10):
        if (self.weight == None):
            self.weight = np.zeros((len(self.matrix), len(self.matrix)))
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[0]):
                if self.matrix[i][j]:
                    self.weight[i][j] = round(random.random() * (max_w-min_w) + min_w, 3)
        return self

    @staticmethod
    def random_strongly_conected(node_count, probability):
        # pass
        while True:
            digraph = DiGraph.random(node_count, probability)

            visited = [0] * node_count
            stack = []

            digraph.dfs_util(0, visited, stack)
            print(visited)
            if all(visited):
                return digraph

    @staticmethod
    def random(node_count: int, probability: float):
        if not 0.0 <= probability <= 1.0:
            raise ValueError(f'p should between 0 and 1, is {probability}')
        if node_count < 1:
            raise ValueError(
                f'n should between larger than 1, is {probability}')
        G = DiGraph(node_count)
        for i in range(node_count):
            for j in range(node_count):
                if i != j and random.random() < probability:
                    G.matrix[i][j] = 1
        return G

    def add_weight_matrix(self, matrix):
        self.weight = matrix
        return self
    
    def add_edge(self, start_point, end_point):
        self.matrix[start_point][end_point] = int(1)

    def remove_edge(self, start_point, end_point):
        self.matrix[start_point][end_point] = int(0)

    def print_matrix(self, ozdobnik=True):
        if ozdobnik:
            print('#'*20)
        for c in self.matrix:
            print(c)
        if ozdobnik:
            print('#'*20)
        return self

    def print(self, weight=False):
        DG = None
        if (not weight):
            DG = nx.from_numpy_array(self.matrix, create_using=nx.DiGraph)
        else:
            DG = nx.DiGraph()
            for i in range(self.matrix.shape[0]):
                    for j in range(self.matrix.shape[0]):
                        if self.matrix[i, j] == 1:
                            DG.add_edge(i, j, weight = self.weight[i, j])
        edge_labels = {(u, v): d['weight'] for u, v, d in DG.edges(data=True)}  
        nx.draw(DG, with_labels=True, pos=nx.circular_layout(DG))
        if(weight):
            nx.draw_networkx_edge_labels(DG, pos=nx.circular_layout(DG), edge_labels=edge_labels)
        plt.figure()
        return self

    def printw(self, ozdobnik=True):
        if ozdobnik:
            print('#'*5, "wagi", '#'*5)
        for c in self.weight:
            print(c)
        if ozdobnik:
            print('#'*20)
        return self

    def transpose(self):
        transposed_graph = DiGraph(self.matrix.shape[1])

        for u in range(self.matrix.shape[0]):
            for v in range(self.matrix.shape[0]):
                transposed_graph.matrix[v][u] = self.matrix[u][v]
        transposed_graph.matrix = transposed_graph.matrix.astype(int)
        return transposed_graph

    def dfs(self, vertex, visited, stack):
        visited[vertex] = True
        for neighbor in range(self.matrix.shape[1]):
            if not visited[neighbor] and self.matrix[vertex][neighbor]:
                self.dfs(neighbor, visited, stack)

        stack.append(vertex)

    def dfs_util(self, vertex, visited, result):
        visited[vertex] = 1
        result.append(vertex)

        for neighbor in range(self.matrix.shape[1]):
            if not visited[neighbor] and self.matrix[vertex][neighbor]:
                self.dfs_util(neighbor, visited, result)

    def kosaraju(self):
        self.matrix = self.matrix.astype(int)
        visited = [False] * self.matrix.shape[0]
        stack = []

        for vertex in range(self.matrix.shape[0]):
            if not visited[vertex]:
                self.dfs(vertex, visited, stack)
                # print("vertex: ",vertex," stack: ", stack, "visited:", visited, )
        transposed_graph = self.transpose()

        visited = [False] * self.matrix.shape[0]
        scc = []

        while stack:
            vertex = stack.pop()
            if not visited[vertex]:
                result = []
                transposed_graph.dfs_util(vertex, visited, result)
                scc.append(result)
        return scc

    def bellmana_forda(self, start:int):
        ds = {node: float('inf') for node in range(self.matrix.shape[0])}
        ds[start] = 0
    
        ps = {node: -1 for node in range(self.matrix.shape[0])}

        for i in range(self.matrix.shape[0]-1):
            for u in range(self.matrix.shape[0]):
                for v in range(self.matrix.shape[0]):
                    if self.matrix[u][v]:
                        if(ds[v]>ds[u]+self.weight[u][v]):
                            ds[v]=ds[u]+self.weight[u][v]
                            ps[v]=u
        for u in range(self.matrix.shape[0]-1):
            for v in range(self.matrix.shape[0]-1):
                if self.matrix[u][v] and ds[v]>ds[u]+self.weight[u][v] :
                    return False , ds
        return True , ds

    def johnson_algorithm(self):
        # Dodajemy wierzchołek źródłowy i krawędzie z wagą 0 do każdego innego wierzchołka
        num_nodes = len(self.matrix)
        extended_matrix = np.zeros((num_nodes + 1, num_nodes + 1))
        extended_weight  = np.zeros((num_nodes + 1, num_nodes + 1))
        for u in range(self.matrix.shape[0]-1):
            for v in range(self.matrix.shape[0]-1):
                extended_matrix[u, v] = self.matrix[u, v]
                extended_weight[u, v] = self.weight[u, v]
        extended_matrix[self.matrix.shape[0] ,:self.matrix.shape[0] ] = 1
    
        # Wykonujemy algorytm Bellmana-Forda
        G = DiGraph().from_neighbourhood_matrix(extended_matrix).add_weight_matrix(extended_weight)
        neg_cyc , ds =  G.bellmana_forda(self.matrix.shape[0])
        if( not neg_cyc):
            raise ValueError('there is a negative cycle in the graph!')
        h = []
        for c in ds:
            h.append(ds[c])
        
        print("h:")
        print(h)
            
        # Aktualizujemy wagi dla wszystkich krawędzi
        for u in range(num_nodes):
            for v in range(num_nodes):
                if extended_weight[u, v] != float('inf') and self.matrix[u, v] ==1 :
                    extended_weight[u, v] = self.weight[u, v] + h[u] - h[v]
        print("pre")
        print( self.weight)
        print("after")
        print( extended_weight)
        
        # Wykonujemy algorytm Dijkstry dla każdego wierzchołka jako źródła
        all_pairs_shortest_paths = {}
        for source in range(num_nodes):
            G = nx.DiGraph()
            for i in range(self.matrix.shape[0]):
                    for j in range(self.matrix.shape[0]):
                        if self.matrix[i, j] == 1:
                            G.add_edge(i, j, weight = extended_weight[i, j])
            distances = nx.single_source_dijkstra_path_length(G, source)
            # Przywracamy poprawne wagi
            for target in range(num_nodes):
                if distances[target] != float('inf'):
                    distances[target] = distances[target] - h[source] + h[target]
            
            all_pairs_shortest_paths[source] = distances
        
        return all_pairs_shortest_paths
if __name__ == '__main__':
    # DiGraph(2)
    # graph = DiGraph().from_neighbourhood_matrix_file(
    #     'data/neighbourhood_di_matrix.txt').print_matrix()
    # graph.print()
    # print(graph.kosaraju())
    # DiGraph.random(8,.5).print_matrix()
    graph = DiGraph().from_neighbourhood_matrix_file(
        'data/neighbourhood_di_matrix_ex1.txt').print_matrix()
    graph.print()
    graph.rand_wages()
    graph.printw()
    print(graph.bellmana_forda(0))
    print("$"*20)
    print(graph.johnson_algorithm())
    # graph.transpose().print()
    # print(graph.kosaraju())

    # R  = DiGraph.random_strongly_conected(9,.3)
    # print(R.print().print_matrix().kosaraju())
