import copy
from euler_and_hamilton import Euler, Hamilton
from graph import Graph, GraphDrawer, check_graphic_sequence, random_regular_graph


def task1_1():
    g = Graph()
    print('is given graph graphic? ', check_graphic_sequence
    (g.from_graphic_sequence_file('./data/graphic_sequence.txt')))


def task1_2():
    g = Graph()
    print('is given graph graphic? ', check_graphic_sequence(g.from_graphic_sequence_file
                                                               ('./data/graphic_sequence2.txt')))


def task2_1():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('before randomization').to_screen()
    g.randomize(10)
    gd.parse(g).with_title('after randomization').to_screen()


def task2_2():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence2.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('before randomization').to_screen()
    g.randomize(10)
    gd.parse(g).with_title('after randomization').to_screen()


def task3_1():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence.txt')
    g.components(True)
    gd = GraphDrawer()
    gd.parse(g).with_title('some graph where we search for components').to_screen()


def task3_2():
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence2.txt')
    g.components(True)
    gd = GraphDrawer()
    gd.parse(g).with_title('some graph where we search for components').to_screen()


def task4():
    e = Euler()
    e.create_graph(8)
    gd = GraphDrawer()
    needed_edges = copy.deepcopy(e.graph.matrix)
    e.set_euler_path()
    e.graph.matrix = needed_edges
    gd.parse(e.graph).with_title('some euler graph').to_screen()


def task5():
    g = random_regular_graph(5, 11)
    gd = GraphDrawer()
    gd.parse(g).with_title('random k-regular graph').to_screen()


def task6_1():
    h = Hamilton()
    h.create_graph([3, 2, 3, 4, 4, 6, 4, 2])
    gd = GraphDrawer()
    h.check_hamilton_path()
    print([i+1 for i in h.stack])
    gd.parse(h.g).with_title('graph to check hamilton cycle').to_screen()


def task6_2():
    h = Hamilton()
    h.create_graph([3, 2, 3, 4, 4, 6, 4, 2, 1, 1])
    gd = GraphDrawer()
    h.check_hamilton_path()
    print([i+1 for i in h.stack])
    gd.parse(h.g).with_title('graph to check hamilton cycle').to_screen()


if __name__ == '__main__':
    try:
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

    except RecursionError as e:
        print('there is no hamilton cycle')
    except Exception as e:
        raise e
