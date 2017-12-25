import analysis
import time
start = time.time()

filenames = ['./data/wiki-Vote/wiki-Vote.txt']

g = analysis.load_graph(filenames[0], directed=True)
print('load graph: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

accuracy = 0.05

print('=====LSCC=====')
start_lscc = time.time()
lscc = analysis.calculate_largest_strongly_connected_comp(g)
print('calculate LSCC: \t', int(divmod(time.time() - start_lscc, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
print('LSCC edges: \t', lscc.num_edges())
print('LSCC nodes: \t', lscc.num_vertices())
print('accuracy is ', accuracy * 100, '% corresponds to ', int(accuracy * lscc.num_vertices()), 'sampled pairs of vertices of LSCC')

lscc_dists = analysis.calculate_distances(lscc, accuracy)
print('caluclate distances LSCC: \t', int(divmod(time.time() - start_lscc, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

s_median, s_mean, s_diam, s_eff_diam = analysis.compute_stats(lscc_dists)
print('median distance:\t', s_median)
print('mean distance:\t\t', s_mean)
print('diameter:\t\t', s_diam)
print('effective diameter:\t', s_eff_diam)
print('LSCC done: \t', int(divmod(time.time() - start_lscc, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
del lscc, lscc_dists

print('=====LWCC=====')
start_lwcc = time.time()
lwcc = analysis.calculate_largest_weakly_connected_comp(g)
print('calculate LWCC: \t', int(divmod(time.time() - start_lwcc, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
print('LWCC edges: \t', lwcc.num_edges())
print('LWCC nodes: \t', lwcc.num_vertices())
print('accuracy is ', accuracy * 100, '% corresponds to ', int(accuracy * lwcc.num_vertices()), 'sampled pairs of vertices of LWCC')

lwcc_dists = analysis.calculate_distances(lwcc, accuracy)
print('caluclate distances LWCC: \t',int(divmod(time.time() - start_lwcc, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

w_median, w_mean, w_diam, w_eff_diam = analysis.compute_stats(lwcc_dists)
print('median distance:\t', w_median)
print('mean distance:\t\t', w_mean)
print('diameter:\t\t', w_diam)
print('effective diameter:\t', w_eff_diam)
print('LWCC done: \t', int(divmod(time.time() - start_lwcc, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

print('complete code: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
