import copy
from euler_and_hamilton import Euler, Hamilton
from graph import Graph, GraphDrawer, check_graphic_sequence, random_regular_graph, BadGraphInput


def task1_1():
    g = Graph()
    gd = GraphDrawer()
    print('is given graph graphic? ', check_graphic_sequence(g.from_graphic_sequence_file('./data/graphic_sequence.txt')))
    if check_graphic_sequence(g.from_graphic_sequence_file('./data/graphic_sequence.txt')):
        gd.parse(g).with_title('example graph').to_screen()


def task1_2():
    g = Graph()
    print('is given graph graphic? ', check_graphic_sequence(g.from_graphic_sequence_file('./data/graphic_sequence2.txt')))
    gd = GraphDrawer()
    if check_graphic_sequence(g.from_graphic_sequence_file('./data/graphic_sequence2.txt')):
        gd.parse(g).with_title('example graph').to_screen()


def task2_1():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('before randomization').to_screen()
    g.randomize(100)
    gd.parse(g).with_title('after randomization').to_screen()


def task2_2():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence2.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('before randomization').to_screen()
    g.randomize(100)
    gd.parse(g).with_title('after randomization').to_screen()


def task3_1():
    g = Graph()
    if not g.from_graphic_sequence_file('./data/graphic_sequence.txt') is None:
        g.from_graphic_sequence_file('./data/graphic_sequence.txt')
        g.components(True)
        gd = GraphDrawer()
        gd.parse(g).with_title('some graph where we search for components').to_screen()
    else:
        raise BadGraphInput('Invalid sequence')


def task3_2():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence2.txt')
    g.components(True)
    gd = GraphDrawer()
    gd.parse(g).with_title('some graph where we search for components').to_screen()


def task4():
    e = Euler()
    e.create_graph(9)
    gd = GraphDrawer()
    needed_edges = copy.deepcopy(e.graph.matrix)
    e.set_euler_path()
    e.graph.matrix = needed_edges
    gd.parse(e.graph).with_title('some euler graph').to_screen()


def task5():
    g = random_regular_graph(4, 12)
    gd = GraphDrawer()
    gd.parse(g).with_title('random k-regular graph').to_screen()


def task6_1():
    h = Hamilton()
    h.create_graph([3, 2, 3, 4, 4, 6, 4, 2])
    gd = GraphDrawer()
    path = h.check_hamilton_path(h.stack)
    if path is None:
        print('There is no Hamiltonian cycle')
    else:
        print('Hamiltonian cycle', [i + 1 for i in path])
    gd.parse(h.g).with_title('simple graph').to_screen()


def task6_2():
    h = Hamilton()
    h.create_graph([5,3,2,5,3,2,4])
    # h.g.randomize(50)
    gd = GraphDrawer()
    path = h.check_hamilton_path(h.stack)
    if path is None:
        print('There is no Hamiltonian cycle')
    else:
        print('Hamiltonian cycle', [i + 1 for i in path])
    gd.parse(h.g).with_title('simple graph').to_screen()


if __name__ == '__main__':
    task1_1()
    task1_2()
    task2_1()
    print('-' * 20)
    task2_2()
    print('-'*20)
    task3_1()
    print('-' * 20)
    task3_2()
    print('-' * 20)
    task4()
    print('-' * 20)
    task5()
    task6_1()
    print('-'*20)
    task6_2()
