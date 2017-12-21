import analysis_nx
import time
start = time.time()

path_to_file = './data/soc-Epinions1/soc-Epinions1.txt'
g = analysis_nx.load_graph(path_to_file, True)
print('load graph: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

LSCC = analysis_nx.calculate_largest_strongly_connected_comp(g)
print('calculate LSCC: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

LWCC = analysis_nx.calculate_largest_weakly_connected_comp(g)
print('calculate LWCC: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

print('LSCC edges: \t', LSCC.number_of_edges())
print('LSCC nodes: \t', LSCC.number_of_nodes())
print('LWCC edges: \t',LWCC.number_of_edges())
print('LWCC nodes: \t',LWCC.number_of_nodes())

LSCC_dist = analysis_nx.compute_shortest_path_distances_parallel_mp(LSCC)
print('caluclate distances LSCC: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

LWCC_dist = analysis_nx.compute_shortest_path_distances_parallel_mp(LWCC)
print('caluclate distances LWCC: \t',int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

s_median, s_mean, s_diam, s_eff_diam = analysis_nx.compute_stats(LSCC_dist)
w_median, w_mean, w_diam, w_eff_diam = analysis_nx.compute_stats(LWCC_dist)

print('=====LSCC=====')
print('median distance: \t', s_median)
print('mean distance: \t', s_mean)
print('diameter: \t', s_diam)
print('effective diameter: \t', s_eff_diam)
print()
print('=====LWCC=====')
print('median distance: \t', w_median)
print('mean distance: \t', w_mean)
print('diameter: \t', w_diam)
print('effective diameter: \t', w_eff_diam)

print('complete code: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
