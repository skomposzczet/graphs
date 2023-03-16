from graph import Graph, GraphDrawer, RandomGraph
import numpy as np

def bigexample1():
    '''Imports neighbourhood matrix from lab examples, and prints all versions'''
    g = Graph()
    g.from_neighbourhood_matrix_file('data/big_neighbourhood_matrix.txt')
    print(np.array(g.as_neighbourhood_matrix()))
    print(g.as_adjacency_list())
    print(np.array(g.as_incidence_matrix()))

def bigexample2():
    '''Imports adjacency list from lab examples, and prints all versions'''
    g = Graph()
    g.from_adjacency_list_file('data/big_adjacency_list.txt')
    print(np.array(g.as_neighbourhood_matrix()))
    print(g.as_adjacency_list())
    print(np.array(g.as_incidence_matrix()))

def bigexample3():
    '''Imports incidence matrix from lab examples, and prints all versions'''
    g = Graph()
    g.from_incidence_matrix_file('data/big_incidence_matrix.txt')
    print(np.array(g.as_neighbourhood_matrix()))
    print(g.as_adjacency_list())
    print(np.array(g.as_incidence_matrix()))

def example1():
    '''Imports neighbourhood matrix from lab presentation, and prints all versions'''
    g = Graph()
    g.from_neighbourhood_matrix_file('data/neighbourhood_matrix.txt')
    print(np.array(g.as_neighbourhood_matrix()))
    print(g.as_adjacency_list())
    print(np.array(g.as_incidence_matrix()))
    
def drawexample1():
    '''Draws neighbourhood matrix from lab examples'''
    g = Graph()
    g.from_neighbourhood_matrix_file('data/big_neighbourhood_matrix.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('in file').to_file('graph.png')

def drawexample2():
    '''Draws neighbourhood matrix from lab presentation'''
    g = Graph()
    g.from_neighbourhood_matrix_file('data/neighbourhood_matrix.txt')
    gd = GraphDrawer()
    gd.parse(g).with_title('some graph').to_screen()

def crazyexample():
    '''Imports neighbourhood matrix from lab examples,
    presents possibility to parse own output
    '''
    g = Graph()
    gd = GraphDrawer()

    g.from_neighbourhood_matrix_file('data/big_neighbourhood_matrix.txt')
    print(g.as_neighbourhood_matrix())
    gd.parse(g).to_screen()

    g.from_incidence_matrix(g.as_incidence_matrix())
    print(g.as_neighbourhood_matrix())
    gd.parse(g).to_screen()

def randomexample1():
    '''Generates four random graphs from lab presentation'''
    gd = GraphDrawer()

    g = RandomGraph.random_nl(20,30)
    gd.parse(g).with_title('n=20 l=30').to_screen()
    g = RandomGraph.random_nl(20,190)
    gd.parse(g).with_title('n=20 l=190').to_screen()
    g = RandomGraph.random_np(20,0.005)
    gd.parse(g).with_title('n=20 p=0.005').to_screen()
    g = RandomGraph.random_np(20,0.5)
    gd.parse(g).with_title('n=20 p=0.5').to_screen()

def randomexample2():
    '''Generates two random graphs from lab examples'''
    gd = GraphDrawer()

    g = RandomGraph.random_nl(7,10)
    gd.parse(g).with_title('n=7 l=10').to_screen()
    g = RandomGraph.random_np(7,0.5)
    gd.parse(g).with_title('n=7 p=0.5').to_screen()

if __name__ == '__main__':
    delim = '*'*50
    try:
        bigexample1()
        print(delim)
        bigexample2()
        print(delim)
        bigexample3()
        print(delim)
        example1()
        print(delim)
        drawexample1()
        drawexample2()
        crazyexample()
        randomexample1()
        randomexample2()
    except Exception as e:
        raise e
    else:
        print('All went great')