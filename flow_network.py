import networkx as nx
from matplotlib import pyplot as plt
import random
from networkx import NetworkXNoCycle
from graph import BadGraphInput


class FlowNetwork:

    def __init__(self):
        self.G = nx.DiGraph()

    def create_graph(self, N: int):
        if N < 2 or N > 4:
            raise BadGraphInput('2,3 or 4 layers expected')

        self.G.add_node('s', layer=0)
        size_of_layers = [1]

        # add nodes to network
        index_alphabet = 0
        for layer in range(1, N+1):
            number_of_nodes = random.randint(2, N)
            size_of_layers.append(number_of_nodes)
            for _ in range(number_of_nodes):
                self.G.add_node(chr(ord('a') + index_alphabet), layer=layer)
                index_alphabet += 1
        self.G.add_node('t', layer=N + 1)
        size_of_layers.append(1)

        # add edges from source to first layer
        for index in range(size_of_layers[1]):
            self.G.add_edge('s', chr(ord('a') + index), weight=random.randint(1, 10))

        # add edges to the middle of layer
        for index in range(1, N):
            current_edge_index = 0
            for edge_number in range(min(size_of_layers[index], size_of_layers[index+1])):
                start_node = chr(ord('a')+current_edge_index+sum(size_of_layers[1:index]))
                end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+current_edge_index)
                self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                current_edge_index += 1

            if size_of_layers[index] > size_of_layers[index+1]:
                for rest in range(size_of_layers[index]-current_edge_index):
                    start_node = chr(ord('a')+sum(size_of_layers[1:index])+current_edge_index)
                    end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+random.randint(0, size_of_layers[index+1]-1))
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1
            else:
                for rest in range(size_of_layers[index+1]-current_edge_index):
                    start_node = chr(ord('a')+sum(size_of_layers[1:index]))
                    end_node = chr(ord('a')+sum(size_of_layers[1:index+1])+current_edge_index)
                    self.G.add_edge(start_node, end_node, weight=random.randint(1, 10))
                    current_edge_index += 1

        # add edges to last layer
        for index in range(size_of_layers[-2]):
            self.G.add_edge(chr(ord('a') + sum(size_of_layers[1:-2])+index), 't', weight=random.randint(1, 10))

        added_edges = 0
        while added_edges < 2*N:
            random_input_layer = random.randint(1, N)
            random_output_layer = random.randint(random_input_layer-1, random_input_layer+1)
            index_input_layer = random.randint(0, size_of_layers[random_input_layer]-1)
            index_output_layer = random.randint(0, size_of_layers[random_output_layer]-1)

            if random_input_layer > 0 and 0 < random_output_layer < N+1:
                input_node = chr(ord('a')+sum(size_of_layers[1:random_input_layer])+index_input_layer)
                output_node = chr(ord('a') + sum(size_of_layers[1:random_output_layer])+index_output_layer)
                if not self.G.has_edge(input_node, output_node) and not self.G.has_edge(output_node, input_node) and input_node != output_node:
                    self.G.add_edge(input_node, output_node, weight=random.randint(1, 10))
                    try:
                        found_cycle = nx.find_cycle(self.G)
                        if found_cycle:
                            self.G.remove_edge(input_node, output_node)
                    except NetworkXNoCycle:
                        added_edges += 1

    def adjacency_matrix(self):
        print('-----------\nadjacency matrix:')
        print(self.G.nodes)
        return nx.adjacency_matrix(self.G).toarray()

    def draw_graph(self):
        pos = nx.multipartite_layout(self.G, subset_key='layer')
        nx.draw(self.G, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, label_pos=0.75, alpha=0.8, font_size=8)
        plt.show()


if __name__ == '__main__':
    pass
