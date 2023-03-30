import random
from graph import Graph, check_graphic_sequence, BadGraphInput


class Euler:

    def __init__(self):
        self.graph = Graph()

    def create_graph(self, size):
        sequence = [random.randrange(2, size, 2) for _ in range(size)]
        print('graph sequence: ', sequence)
        if not check_graphic_sequence(sequence):
            raise BadGraphInput('graph is not graphic')
        self.graph.from_graphic_sequence(sequence)

    def set_euler_path(self):
        # https://cp-algorithms.com/graph/euler_path.html#algorithm
        stack = [0]
        answer = []
        while len(stack) != 0:
            v = stack[-1]
            if 1 not in self.graph.matrix[v]:
                answer.append(v)
                stack.pop()
            else:
                edge = self.graph.matrix[v].index(1)
                self.graph.matrix[v][edge] = 0
                self.graph.matrix[edge][v] = 0
                stack.append(edge)
        print([[i+1] for i in answer])


class Hamilton:

    def __init__(self):
        self.stack = [0]
        self.g = Graph()
        self.visited = []

    def create_graph(self, graphic_sequence):
        if check_graphic_sequence(graphic_sequence):
            self.g.from_graphic_sequence(graphic_sequence)
            if self.g.components() != 1:
                raise BadGraphInput('more than one component in graph')
            self.visited = [-1 for _ in self.g.matrix]
            self.visited[0] = 1
        else:
            raise BadGraphInput('it is not graphic sequence')

    def check_hamilton_path(self):
        if len(self.stack) == len(self.visited):
            if self.g.matrix[self.stack[0]][self.stack[-1]] == 1:
                self.stack.append(self.stack[0])
            else:
                self.visited[self.stack[-1]] = -1
                self.stack.pop()
                self.check_hamilton_path()
        else:
            for edge_index in range(1, len(self.g.matrix)):
                if self.g.matrix[self.stack[-1]][edge_index] == 1 and self.visited[edge_index] == -1:
                    self.stack.append(edge_index)
                    self.visited[edge_index] = 1
                    self.check_hamilton_path()

            if len(self.stack) < len(self.g.matrix):
                self.visited[self.stack[-1]] = -1
                self.stack.pop()
