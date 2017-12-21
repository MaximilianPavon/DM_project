import numpy as np
import networkx as nx
# for parallelisation
import multiprocessing as mp
from functools import partial

def load_graph(filename, directed=True):
    if directed:
        g = nx.read_edgelist(filename, comments='#', delimiter='\t', nodetype=int, create_using=nx.DiGraph())
    else:
        g = nx.read_edgelist(filename, comments='#', delimiter='\t', nodetype=int)
    return g

def calculate_largest_strongly_connected_comp(g):
    return max(nx.strongly_connected_component_subgraphs(g), key=len)

def calculate_largest_weakly_connected_comp(g):
    return  nx.to_undirected(max(nx.weakly_connected_component_subgraphs(g), key=len))

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
