from euler import Euler
from graph import Graph, GraphDrawer, check_graphic_sequence, random_regular_graph


def task1():
    """checks sequence"""
    g = Graph()
    print(check_graphic_sequence(g.from_graphic_sequence_file('./data/graphic_sequence2.txt')))


def task2():
    """randomizes edges"""
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('before randomization').to_screen()
    g.randomize(10)
    gd.parse(g).with_title('after randomization').to_screen()


def task3():
    """finds components of graph"""
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence2.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('some graph where we search for components').to_screen()
    print(g.components())


def task4():
    e = Euler()
    e.create_graph(8)
    gd = GraphDrawer()
    gd.parse(e.graph).with_title('some euler graph').to_screen()
    e.set_euler_path()


def task5():
    g = random_regular_graph(10, 11)
    gd = GraphDrawer()
    gd.parse(g).with_title('random k-regular graph').to_screen()


if __name__ == '__main__':
    try:
        # task1()
        # task2()
        # task3()
        # task4()
        task5()

    except Exception as e:
        raise e
