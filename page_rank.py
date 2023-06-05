import numpy as np
    
def page_rank(graph, iterations=100, damping_factor=0.85):
    num_nodes = len(graph)
    initial_rank = 1 / num_nodes

    # Inicjalizacja wartości PageRank dla każdego węzła
    page_rank = {node: initial_rank for node in graph}

    for _ in range(iterations):
        new_page_rank = {}
        for node in graph:
            incoming_nodes = [incoming_node for incoming_node in graph if node in graph[incoming_node]]

            rank_sum = 0
            for incoming_node in incoming_nodes:
                outgoing_degree = len(graph[incoming_node])
                rank_sum += page_rank[incoming_node] / outgoing_degree

            new_page_rank[node] = (1 - damping_factor) / num_nodes + damping_factor * rank_sum

        page_rank = new_page_rank

    return page_rank

def page_rank_random_walk(graph, d=0.15, iterations=100):
    num_nodes = len(graph)
    transition_matrix = np.zeros((num_nodes, num_nodes))

    for i, node in enumerate(graph):
        outgoing_nodes = graph[node]
        num_outgoing = len(outgoing_nodes)

        for neighbor in outgoing_nodes:
            j = list(graph.keys()).index(neighbor)
            transition_matrix[j, i] = 1 / num_outgoing

    page_rank = np.ones(num_nodes) / num_nodes

    for _ in range(iterations):
        page_rank = (1 - d) * np.dot(transition_matrix, page_rank) + d / num_nodes

    return page_rank



if __name__ == '__main__':
    graph = {
        'A': ['E','F','I'],
        'B': ['A','C','F'],
        'C':  ['B' , 'D', 'E' , 'L'],
        'D' : ['C' , 'E' , 'H' , 'I' , 'K'],
        'E' : ['C' , 'G' , 'H' , 'I'],
        'F' : ['B' , 'G'],
        'G' : ['E' , 'F' , 'H'],
        'H' : ['D' , 'G' , 'I' , 'L'],
        'I' : ['D' , 'E' , 'H' , 'J'],
        'J' : ['I'],
        'K' : ['D' , 'I'],
        'L' : ['A' , 'H']
    }
    pr = page_rank(graph)
    pr_s = sorted(pr.items(), key= lambda x:x[1])
    print(*pr_s, sep='\n')
    
    damping_factor = 0.15
    iterations = 100

    tab = [] 
    i = 0 
    page_rank_random = page_rank_random_walk(graph, damping_factor, iterations)
    for a in page_rank_random:
        tab.append((chr(ord('A')+i) , a))
        i+=1
    # print(tab)
    tab_s = sorted(tab, key= lambda x:x[1])
    print("teleportation metod")
    print(*tab_s, sep='\n')
    # print("PageRank (metoda błądzenia przypadkowego z teleportacją):")
    # print(page_rank_random)