import analysis_nx
import networkx as nx
import random
import numpy as np


def cache_graph():
    g = analysis_nx.load_graph('data/wiki-Vote/wiki-Vote.txt')
    lscc = analysis_nx.calculate_largest_strongly_connected_comp(g)
    lwcc = analysis_nx.calculate_largest_weakly_connected_comp(g)
    nx.write_gpickle(g, 'graphs/wiki-g.gpickle')
    nx.write_gpickle(lscc, 'graphs/wiki-lscc.gpickle')
    nx.write_gpickle(lwcc, 'graphs/wiki-lwcc.gpickle')


def read_cached(graph_name):
    """
    :param str graph_name: Graph filename
    :return: The loaded graph
    :rtype: nx.Graph
    """
    return nx.read_gpickle('graphs/' + graph_name + '.gpickle')


def method_2(g, n_samples):
    """
    BFS thing
    :param nx.Graph g: Graph
    :param int n_samples: Number of samples
    :return: A view of the bfs_thing graph
    """
    print('taking', n_samples, 'samples')
    bfs_edges = []

    for _ in range(n_samples):
        source = random.choice(list(g.nodes()))
        bfs_edges.extend(list(nx.bfs_edges(g, source)))

    return g.edge_subgraph(bfs_edges)


def method_3(g, n_samples):
    k = L = g.number_of_nodes()
    bitmaps = np.zeros((k, L), dtype=np.bool)

    for j in range(n_samples):
        for i in 0:
            for kk in 0:
                pass


def compute_index():
    pass


def leftmost_zero(array):
    nz_is = np.nonzero(array)[0]
    assert nz_is.size != 0, 'Everything is zero!'
    return len(array) - nz_is[-1] - 1


if __name__ == "__main__":
    #g = read_cached('wiki-g')
    #lscc = read_cached('wiki-lscc')
    #lwcc = read_cached('wiki-lwcc')
    g = analysis_nx.load_graph('data/wiki-Vote/wiki-Vote.txt')
    lscc = analysis_nx.calculate_largest_strongly_connected_comp(g)
    lwcc = analysis_nx.calculate_largest_weakly_connected_comp(g)

    n_samples = int(0.01 * lscc.number_of_nodes())
    bfs_graph = method_2(lscc, n_samples)
