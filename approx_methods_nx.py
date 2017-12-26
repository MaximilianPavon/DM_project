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


def method_3(g, n_samples=32, max_iter=256):
    """
    section 2.2 http://math.cmu.edu/~ctsourak/tkdd10.pdf
    """
    K = n_samples
    max_iter = max_iter # h
    n = g.number_of_nodes() # i
    L = 64 # length of the bitstring
    bitmaps = np.zeros((K, max_iter, n, L), dtype=np.bool)

    h_max = -1
    N = np.zeros(max_iter)

    for h in range(max_iter):
        changed = False
        for i in range(n):
            for l in range(K):
                bitmaps[l, h, i] = bitmaps[l, h - 1, i] | 'thefuck'

            if 'something not equal to something':
                changed = True

        N[h] = _neighborhood_sum(bitmaps, n, K, h)
        if not changed:
            h_max = h
            break # the loop

    eff_diameter = 'smallest strange thing'

    return 0


def _neighborhood_sum(b, n, k, h):
    neigh_sum = 0
    for ii in range(n):
        neigh_sum += neighborhood_func(b, k, h, ii)

    return neigh_sum


def neighborhood_func(b, k, h, i):
    s = 0
    for l in range(k):
        s += leftmost_zero(b[l, h, i])
    return 2 ** (s / k) / 0.77351


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

    #method_3(g, 32)
