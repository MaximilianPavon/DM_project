from graph_tool.all import *
from graph_tool import topology
import math
import csv
import itertools
import numpy as np

def nCr(n,r):
    '''Compute the number of combinations of n taking r'''
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def load_graph(filename, directed=True):
    g = Graph(directed=directed)
    
    with open(filename) as f:
        reader_network = csv.reader(f, delimiter='\t', skipinitialspace=True)
        g.add_edge_list(map(int, edge) for edge in reader_network)
    
    return g

def calculate_largest_strongly_connected_comp(g):
    l = topology.label_largest_component(g, directed=True)
    return GraphView(g, vfilt=l, directed=True)

def calculate_largest_weakly_connected_comp(g):
    w = topology.label_largest_component(g, directed=False)
    return GraphView(g, vfilt=w, directed=False)

def calculate_distances(g):
    g_distances = topology.shortest_distance(g)
    dist = []
    counter = 0
    
    if g.is_directed():
        all_pairs = itertools.permutations(g.vertices(), 2)
        num_pairs = g.num_vertices() ** 2
    else:
        all_pairs = itertools.combinations(g.vertices(), 2)
        num_pairs = nCr(g.num_vertices(), 2)

    for (v1, v2) in all_pairs:
        dist.append(g_distances[v1][v2])

        if (counter % 2000000 == 0):
            print(counter / num_pairs * 100, '%')
        counter = counter + 1
    
    return dist

def compute_stats(dist):
    return np.percentile(dist, 50), np.mean(dist), np.max(dist), np.percentile(dist, 90)
