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


def method_3(g, num_bitstrings=8, max_iter=64, len_bitstrings=64):
    """
    section 2.2 http://math.cmu.edu/~ctsourak/tkdd10.pdf
    """
    nodes = nx.nodes(g)
    num_nodes = np.max(nodes) + 1

    bitmaps = np.zeros((num_bitstrings, max_iter, num_nodes, len_bitstrings), dtype=np.bool)

    for node in nodes:
        for l in range(num_bitstrings):
            bitmaps[l, 0, node] = np.array(list(np.binary_repr(len(list(nx.neighbors(g, node))), width=len_bitstrings))).astype(bool)

    h_max = -1
    neighborhood = np.zeros(max_iter)

    for h in range(1, max_iter):
        changed = 0
        for node in nodes:
            for l in range(1, num_bitstrings):
                neighbors = nx.neighbors(g, node)
                bitmaps[l, h, node] = bitmaps[l, h - 1, node]
                for neighbor in neighbors:
                    bitmaps[l, h, node] |= bitmaps[l, h - 1, neighbor]

            for l in range(1, num_bitstrings):
                if not np.array_equal(bitmaps[l, h, node], bitmaps[l, h - 1, node]):
                    changed += 1

        neighborhood[h] = neighborhood_sum(bitmaps, nodes, num_bitstrings, h)
        if changed == 0:
            h_max = h
            break

    print('diameter of the component: {}'.format(h_max))
    print('mean distance of the component: {}'.format(int(np.mean(neighborhood))))
    # smallest_h = -1
    # perfect_match = False
    # for h in range(max_iter):
    #     if neighborhood[h] == 0.9 * neighborhood[h_max]:
    #         perfect_match = True
    #         smallest_h = h
    #         break
    #     elif neighborhood[h] > 0.9 * neighborhood[h_max]:
    #         smallest_h = h
    #         break
    #
    # if perfect_match:
    #     print('effective diameter: ', smallest_h)
    # else:
    #     print('effective diameter: ', statistics.interpolate(smallest_h, h_max, neighborhood))


def neighborhood_sum(b, n, k, h):
    neigh_sum = 0
    for ii in n:
        neigh_sum += neighborhood_func(b, k, h, ii)

    return neigh_sum


def neighborhood_func(b, k, h, i):
    s = 0
    for l in range(k):
        s += leftmost_zero(b[l, h, i])
    return 2 ** (s / k) / 0.77351


def leftmost_zero(array):
    for pos in range(len(array)):
        if not array[pos]:
            return len(array) - pos


def interpolate(h, h_max, n_func):
    diameter_eff = h - 1
    diameter_eff += (0.9 * n_func[h_max] - n_func[h - 1]) / (n_func[h] - n_func[h - 1])
    return diameter_eff


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
