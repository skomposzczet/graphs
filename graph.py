from __future__ import annotations

from operator import itemgetter

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
from itertools import combinations
import random


def _get_lines(filename):
    with open(filename) as fh:
        lines = fh.readlines()
    return lines


class BadGraphInput(Exception):
    def __init__(self, message: str):
        super().__init__(f'Graph could not be create due to bad input: {message}')


class Graph:
    def __init__(self):
        self.matrix = None

    def from_neighbourhood_matrix_file(self, filename: str):
        input = _get_lines(filename)
        self.from_neighbourhood_matrix([[int(val) for val in line.split(' ')] for line in input])

    def from_neighbourhood_matrix(self, matrix: list):
        self.matrix = matrix
        self.validate()

    def from_adjacency_list_file(self, filename: str):
        input = _get_lines(filename)
        adj_list = {}
        for line in input:
            index, rest = line.split(':')
            adj_list[int(index)] = [int(v) for v in rest.split(' ')]

        self.from_adjacency_list(adj_list)

    def from_adjacency_list(self, adj_list: dict):
        node_count = len(adj_list)
        matrix = [[0] * node_count for _ in range(node_count)]
        for node, neighbours in adj_list.items():
            for neigh in neighbours:
                matrix[node - 1][neigh - 1] += 1

        self.matrix = matrix
        self.validate()

    def from_incidence_matrix_file(self, filename: str):
        input = _get_lines(filename)
        inc_matrix = [[int(val) for val in line.split(' ')] for line in input]
        self.from_incidence_matrix(inc_matrix)

    def from_incidence_matrix(self, inc_matrix: list):
        node_count = len(inc_matrix)
        matrix = [[0] * node_count for _ in range(node_count)]
        inc_matrix = np.transpose(np.array(inc_matrix))

        for edge in inc_matrix:
            neigbours = [i for i, node in enumerate(edge) if node == 1]

            if len(neigbours) != 2:
                raise BadGraphInput(f'invalid edge, {len(neigbours)} nodes')

            matrix[neigbours[0]][neigbours[1]] += 1
            matrix[neigbours[1]][neigbours[0]] += 1

        self.matrix = matrix
        self.validate()

    def validate(self):
        if any([self.matrix[i][i] for i in range(len(self.matrix))]):
            self.matrix = None
            raise BadGraphInput("can't have loops")
        if any([v > 1 for row in self.matrix for v in row], ):
            self.matrix = None
            raise BadGraphInput("can't have multiple edges")
        if not np.array_equal(np.transpose(np.array(self.matrix)), np.array(self.matrix)):
            self.matrix = None
            raise BadGraphInput("incorrect graph")

    def as_neighbourhood_matrix(self):
        return self.matrix

    def as_adjacency_list(self):
        return {i + 1: [j + 1 for j, v in enumerate(row) if v == 1] for i, row in enumerate(self.matrix)}

    # below in class Graph there are methods created for task 2

    def as_incidence_matrix(self):
        """converts graphical sequence to incidence matrix"""
        edge_count = sum(sum(row) for row in self.matrix) // 2
        node_count = len(self.matrix)

        matrix = [[0] * edge_count for _ in range(node_count)]

        current_edge = 0
        for i in range(len(self.matrix) - 1):
            for j in range(i + 1, len(self.matrix[0])):
                if self.matrix[i][j] == 1:
                    matrix[i][current_edge] = 1
                    matrix[j][current_edge] = 1
                    current_edge += 1

        return matrix

    def from_matrix_to_graphic_sequence(self):
        """converts incidence matrix to graphic sequence"""
        graphic_sequence = []
        for i in self.matrix:
            graphic_sequence.append(i.count(1))
        return graphic_sequence

    def from_graphic_sequence_file(self, filename: str):
        """reads graphic sequence from given file"""
        input = _get_lines(filename)
        graphic_sequence = [int(val) for val in str(input) if val.isdigit()]
        if check_graphic_sequence(graphic_sequence):
            self.from_graphic_sequence(graphic_sequence)
        return graphic_sequence

    def from_graphic_sequence(self, graphic_sequence):
        """converts graphic sequence to incidence matrix"""
        graphic_sequence.sort(reverse=True)
        matrix = [[0 for _ in range(len(graphic_sequence))] for _ in range(len(graphic_sequence))]
        indexes_with_degrees = [[i, graphic_sequence[i]] for i in range(len(graphic_sequence))]
        for i in range(len(graphic_sequence)):
            indexes_with_degrees.sort(reverse=True, key=itemgetter(1))
            for j in range(1, indexes_with_degrees[0][1] + 1):
                indexes_with_degrees[j][1] -= 1
                indexes_with_degrees[0][1] -= 1
                matrix[indexes_with_degrees[j][0]][indexes_with_degrees[0][0]] = 1
                matrix[indexes_with_degrees[0][0]][indexes_with_degrees[j][0]] = 1
        self.matrix = matrix

    def randomize(self, iterations):
        """randomizes edges in graph"""
        count = 0
        while count < iterations:
            a, b, c, d = random.sample(range(0, len(self.matrix)), 4)
            if self.matrix[a][b] == self.matrix[c][d] == 1 and self.matrix[a][d] == self.matrix[c][b] == 0:
                self.matrix[a][b] = self.matrix[c][d] = 0
                self.matrix[b][a] = self.matrix[d][c] = 0
                self.matrix[a][d] = self.matrix[c][b] = 1
                self.matrix[d][a] = self.matrix[b][c] = 1
                count += 1

    def components(self):
        """finds all components in graph"""
        nr = 0
        comp = [-1 for _ in range(len(self.matrix))]

        for edge in range(len(self.matrix)):
            if comp[edge] == -1:
                nr += 1
                comp[edge] = nr
                self.components_R(nr, edge, self.matrix, comp)

        occurences = []
        for element in range(len(self.matrix)):
            counter = comp.count(element)
            if counter:
                occurences.append(counter)

        for index in range(len(occurences)):
            print('\n', index+1, ':', end=' ')
            for edge_number in range(len(comp)):
                if comp[edge_number] == index+1:
                    print(edge_number+1, end=' ')
        print('\nThe longest component: ', max(set(comp), key=comp.count))

    def components_R(self, nr, v, matrix, comp):
        """implements depth-first search (DFS)"""
        for edge in range(len(matrix[v])):
            if v != edge and matrix[v][edge] and comp[edge] == -1:
                comp[edge] = nr
                self.components_R(nr, edge, matrix, comp)


class GraphDrawer:
    def __init__(self):
        self.graph = None
        self.r = 1.
        self.xy = [0., 0.]
        self.title = ''

    def parse(self, graph: Graph) -> GraphDrawer:
        adj_list = graph.as_adjacency_list()
        g = nx.Graph()
        for node, neighs in adj_list.items():
            if not neighs:
                g.add_node(node)
                continue
            for neigh in neighs:
                g.add_edge(node, neigh)
        self.graph = g
        return self

    def with_title(self, title: str) -> GraphDrawer:
        self.title = title
        return self

    def to_screen(self):
        self.__draw()
        plt.show()
        GraphDrawer.__plt_close()

    def to_file(self, filename: str):
        self.__draw()
        plt.savefig(filename)
        GraphDrawer.__plt_close()

    def __plt_close():
        plt.clf()
        plt.cla()
        plt.close()

    def __draw(self):
        if self.graph is None:
            raise TypeError('Graph to draw is None')
        circ = plt.Circle((self.xy[0], self.xy[1]), self.r, color='r', fill=False, linestyle=':')
        _, ax = plt.subplots()
        ax.add_patch(circ)
        nx.draw(self.graph,
                pos=self.__make_pos(),
                labels=None,
                node_color='#D3D3D3'
                )
        plt.axis('scaled')
        plt.title(self.title)

    def __make_pos(self) -> dict:
        nodes = sorted(self.graph.nodes())
        alpha = 2 * math.pi / len(nodes)
        result = {}

        for i, node in enumerate(nodes):
            x = self.xy[0] + self.r * math.sin(i * alpha)
            y = self.xy[1] + self.r * math.cos(i * alpha)
            result[node] = np.array([x, y])

        return result


class RandomGraph:
    def random_nl(node_count: int, edge_count: int) -> Graph:
        if not 0 <= edge_count <= node_count * (node_count - 1) / 2:
            raise ValueError(f'l should be in [0, n(n-1)/2], is n={node_count};l={edge_count}')
        possible_egdes = list(combinations(range(node_count), 2))
        return RandomGraph.from_edges(random.sample(possible_egdes, edge_count), node_count)

    def random_np(node_count: int, probability: float) -> Graph:
        if not 0.0 <= probability <= 1.0:
            raise ValueError(f'p should between 0 and 1, is {probability}')
        possible_egdes = list(combinations(range(node_count), 2))
        return RandomGraph.from_edges([edge for edge in possible_egdes if random.random() < probability], node_count)

    def from_edges(edges: list, n: int) -> Graph:
        matrix = [[0] * n for _ in range(n)]
        for edge in edges:
            i, j = edge
            matrix[i][j] = 1
            matrix[j][i] = 1

        g = Graph()
        g.from_neighbourhood_matrix(matrix)
        return g


def check_graphic_sequence(graphic_sequence) -> bool:
    """task2, checks whether given sequence is graphical"""
    graphic_sequence_copy = graphic_sequence.copy()
    graphic_sequence_copy.sort(reverse=True)

    while True:
        if not np.array(graphic_sequence_copy).any():
            return True

        if graphic_sequence_copy[0] >= len(graphic_sequence_copy) or graphic_sequence_copy[-1] < 0:
            return False

        for i in range(1, int(graphic_sequence_copy[0]) + 1):
            graphic_sequence_copy[i] -= 1

        graphic_sequence_copy[0] = 0
        graphic_sequence_copy.sort(reverse=True)


if __name__ == '__main__':
    pass
