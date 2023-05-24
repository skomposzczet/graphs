import networkx as nx
from matplotlib import pyplot as plt
import random
from graph import BadGraphInput


class FlowNetwork:

    def __init__(self):
        self.G = nx.DiGraph()

    def create_graph(self, N: int):
        if N < 2:
            raise BadGraphInput('not enough layers')

        self.G.add_node('s', layer=0)
        self.G.add_node('t', layer=N+1)
        size_of_layers = [1]

        index_alphabet = 0
        for layer in range(1, N+1):
            number_of_nodes = random.randint(2, N)
            size_of_layers.append(number_of_nodes)
            for _ in range(number_of_nodes):
                self.G.add_node(chr(ord('a') + index_alphabet), layer=layer)
                index_alphabet += 1
        size_of_layers.append(1)

        # add edges from source to first layer
        for index in range(size_of_layers[1]):
            self.G.add_edge('s', chr(ord('a') + index), weight=random.randint(1, 10))

        # add edges in the middle of network
        for index in range(1, N):
            if size_of_layers[index] == size_of_layers[index+1]:
                current_edge_index = 0
                for edge_number in range(size_of_layers[index]):
                    start_node = chr(ord('a')+current_edge_index+sum(size_of_layers[1:index]))
                    end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+current_edge_index)
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1
                    # print(start_node, end_node, index)

            elif size_of_layers[index] > size_of_layers[index+1]:
                current_edge_index = 0
                for edge_number in range(size_of_layers[index+1]):
                    start_node = chr(ord('a')+current_edge_index+sum(size_of_layers[1:index]))
                    end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+current_edge_index)
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1
                    # print(start_node, end_node, index)

                for rest in range(size_of_layers[index]-current_edge_index):
                    start_node = chr(ord('a')+sum(size_of_layers[1:index])+current_edge_index)
                    end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+random.randint(0, size_of_layers[index+1]-1))
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1
                    # print(start_node, end_node, index, rest)

            else:
                current_edge_index = 0
                for edge_number in range(size_of_layers[index]):
                    start_node = chr(ord('a') + current_edge_index + sum(size_of_layers[1:index]))
                    end_node = chr(ord('a') + sum(size_of_layers[1:index + 1]) + current_edge_index)
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1
                    # print(start_node, end_node, index)

                for rest in range(size_of_layers[index+1]-current_edge_index):
                    start_node = chr(ord('a')+sum(size_of_layers[1:index]))
                    end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+current_edge_index)
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1
                    # print(start_node, end_node, index, rest)


        # add edges to last layer
        for index in range(size_of_layers[-2]):
            self.G.add_edge(chr(ord('a') + sum(size_of_layers[1:-2])+index), 't', weight=random.randint(1, 10))

    def draw_graph(self):
        pos = nx.multipartite_layout(self.G, subset_key='layer')
        nx.draw(self.G, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()


if __name__ == '__main__':
    a = FlowNetwork()
    a.create_graph(4)
    a.draw_graph()
