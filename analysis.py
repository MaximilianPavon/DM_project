from graph_tool.all import *
from graph_tool import topology
import math
import csv
import itertools
import numpy as np
import random

def nCr(n,r):
    '''Compute the number of combinations of n taking r'''
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def load_graph(filename, directed=True, delimiter='\t'):
    g = Graph(directed=directed)

    with open(filename) as f:
        reader_network = csv.reader(f, delimiter=delimiter, skipinitialspace=True)
        g.add_edge_list(map(int, edge) for edge in reader_network)

    return g

def calculate_largest_strongly_connected_comp(g):
    l = topology.label_largest_component(g, directed=True)
    return GraphView(g, vfilt=l, directed=True)

def calculate_largest_weakly_connected_comp(g):
    w = topology.label_largest_component(g, directed=False)
    return GraphView(g, vfilt=w, directed=False)

def calculate_distances(g, acc_param=0, g_distances=None):
    if g_distances == None:
        print('start calculate distances')
        g_distances = topology.shortest_distance(g)
        print('calculate distances done')
    else:
        print('use provided distances topology')
        g_distances = g_distances

    dist = []
    counter = 0

    if acc_param>0:
        if g.is_directed():
            all_pairs = n_random_permutations(g.vertices(), int(acc_param * g.num_vertices()))
            num_pairs = int(acc_param * g.num_vertices())
        else:
            all_pairs = n_random_combinations(g.vertices(), int(acc_param * g.num_vertices()))
            num_pairs = int(acc_param * g.num_vertices())
    else:
        if g.is_directed():
            all_pairs = itertools.permutations(g.vertices(), 2)
            num_pairs = g.num_vertices() ** 2
        else:
            all_pairs = itertools.combinations(g.vertices(), 2)
            num_pairs = nCr(g.num_vertices(), 2)

    print('select pairs of permutations/combinations done')

    for (v1, v2) in all_pairs:
        dist.append(g_distances[v1][v2])

        if (counter % int(num_pairs / 20) == 0):
            print(round(counter / num_pairs * 100,1), '%')
        counter = counter + 1

    return dist

def compute_stats(dist):
    return np.percentile(dist, 50), np.mean(dist), np.max(dist), np.percentile(dist, 90)

def n_random_permutations(iterable, n, k=2):
    r_pairs = []
    iterable = tuple(iterable)
    for i in range(n):
        r_pairs.append(tuple(random.sample(tuple(iterable), k)))
    return r_pairs

def n_random_combinations(iterable,n,r=2):
    r_pairs = []
    iterable = tuple(iterable)
    for i in range(n):
        r_pairs.append(random_combination(iterable, r))
    return r_pairs

def random_combination(iterable, r=2):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)
