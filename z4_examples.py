from flow_network import *


def outstanding_example():
    """
    let's have a few random graphs and check if it works fine
    """
    for _ in range(5):
        a = FlowNetwork()
        num = random.randint(2, 4)
        a.create_graph(num)
        print(a.adjacency_matrix())
        a.draw_graph()


if __name__ == '__main__':
    outstanding_example()
