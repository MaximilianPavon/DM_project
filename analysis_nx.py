import numpy as np
import networkx as nx
import multiprocessing as mp  # for parallelisation
from functools import partial
import random


def load_graph(filename, directed=True):
    graph_container = None

    if directed:
        graph_container = nx.DiGraph()

    return nx.read_edgelist(filename, comments='#', delimiter='\t', nodetype=int, create_using=graph_container)


def calculate_largest_strongly_connected_comp(g):
    """
    LSCC
    :param nx.Graph g: Graph
    :return: A view of the LSCC graph
    """
    return max(nx.strongly_connected_component_subgraphs(g, copy=False), key=len)


def calculate_largest_weakly_connected_comp(g):
    """
    LWCC
    :param nx.Graph g: Graph
    :return: A view of the LWCC graph
    """
    return nx.to_undirected(max(nx.weakly_connected_component_subgraphs(g, copy=False), key=len))


def compute_shortest_path_distances_parallel_mp(graph):
    num_cores = mp.cpu_count()
    print(num_cores, 'cores used')

    pool = mp.Pool(processes=num_cores)

    parallel_function = partial(nx.single_source_shortest_path_length, graph)
    sources = [source for source in graph]
    shortest_paths = pool.map(parallel_function, sources)

    pool.close()
    pool.join()

    distances = []
    for _dict in shortest_paths:
        for key, value in _dict.items():
            distances.append(value)

    return distances


def compute_stats(dist):
    return np.percentile(dist, 50), np.mean(dist), np.max(dist), np.percentile(dist, 90)


def n_random_permutations(iterable, n, r=2):
    r_pairs = []

    for i in range(n):
        r_pairs.append(tuple(random.sample(tuple(iterable), r)))

    return r_pairs
