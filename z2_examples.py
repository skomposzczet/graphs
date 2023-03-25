from graph import Graph, GraphDrawer, check_graphic_sequence


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
    g.randomize(100)
    gd.parse(g).with_title('after randomization').to_screen()


def task3():
    """finds components of graph"""
    g = Graph()
    g.from_graphic_sequence_file('./data/graphic_sequence2.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('some graph where we search for components').to_screen()
    g.components()


if __name__ == '__main__':
    try:
        task1()
        task2()
        task3()

    except Exception as e:
        raise e
