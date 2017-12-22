import analysis_nx
import time
start = time.time()

path_to_file = './data/wiki-Vote/wiki-Vote.txt'
g = analysis_nx.load_graph(path_to_file, True)

acc_param = 0.01

node_list = []
for node in g.node():
    node_list.append(node)

num_of_rand_samples = int(g.number_of_nodes() * acc_param)

rand_pairs = analysis_nx.n_random_permutations(node_list, num_of_rand_samples)
