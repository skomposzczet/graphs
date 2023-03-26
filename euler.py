import random
from graph import Graph
from graph import check_graphic_sequence


class Euler:

    def __init__(self):
        self.graph = Graph()

    def create_graph(self, size):
        sequence = [random.randrange(2, size, 2) for _ in range(size)]
        print('graph sequence: ', sequence)
        if check_graphic_sequence(sequence):
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
