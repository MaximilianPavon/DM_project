import analysis
import time
import matplotlib as mpl
import matplotlib.pyplot as plt

from graph_tool.all import *
from graph_tool import topology

start = time.time()
filenames = ['./data/soc-Epinions1/soc-Epinions1.txt']

g = analysis.load_graph(filenames[0], directed=True)
print('vertices:', g.num_vertices(), 'edges:', g.num_edges())
print('load graph: ', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

lscc = analysis.calculate_largest_strongly_connected_comp(g)
lwcc = analysis.calculate_largest_weakly_connected_comp(g)
print('calculate connected components: ', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

print('start calculate distances')
lscc_distances = topology.shortest_distance(lscc)
print('caluclate distances LSCC: ', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
lwcc_distances = topology.shortest_distance(lwcc)
print('caluclate distances LWCC: ', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')

#acc_ar = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7]
acc_ar = [0.01, 0.02, 0.03]
s_median_ar, s_mean_ar, s_diam_ar, s_eff_diam_ar = [], [], [], []
w_median_ar, w_mean_ar, w_diam_ar, w_eff_diam_ar = [], [], [], []
i = 1

for accuracy in acc_ar:

    start_acc = time.time()

    print('=====LSCC=====')
    print('accuracy is ', accuracy * 100, '% corresponds to ', int(accuracy * lscc.num_vertices()), 'sampled pairs of vertices of LSCC')

    lscc_dists = analysis.calculate_distances(lscc, accuracy, lscc_distances)
    s_median, s_mean, s_diam, s_eff_diam = analysis.compute_stats(lscc_dists)
    s_median_ar.append(s_median)
    s_mean_ar.append(s_mean)
    s_diam_ar.append(s_diam)
    s_eff_diam_ar.append(s_eff_diam)


    print('=====LWCC=====')
    print('accuracy is ', accuracy * 100, '% corresponds to ', int(accuracy * lwcc.num_vertices()), 'sampled pairs of vertices of LWCC')

    lwcc_dists = analysis.calculate_distances(lwcc, accuracy, lwcc_distances)
    w_median, w_mean, w_diam, w_eff_diam = analysis.compute_stats(lwcc_dists)
    w_median_ar.append(w_median)
    w_mean_ar.append(w_mean)
    w_diam_ar.append(w_diam)
    w_eff_diam_ar.append(w_eff_diam)

    print('accuracy iteration ',i ,':', int(divmod(time.time() - start_acc, 60)[0]), 'min:', int(divmod(time.time() - start_acc, 60)[1]),'s')

# enter exact values for soc-Epinions1:
s_ex_median, s_ex_mean, s_ex_dia, s_ex_eff_dia = 4, 4.405, 16, 6
w_ex_median, w_ex_mean, w_ex_dia, w_ex_eff_dia = 4, 4.308, 15, 5

plt.figure(figsize=(12,6))
plt.plot(acc_ar, s_median_ar, label='Median distance', color='navy')
plt.axhline(s_ex_median, linestyle='dashed', color='navy')

plt.plot(acc_ar, s_mean_ar, label='Mean distance', color='r')
plt.axhline(s_ex_mean, linestyle='dashed', color='r')

plt.plot(acc_ar, s_diam_ar, label='Diameter', color='orange')
plt.axhline(s_ex_dia, linestyle='dashed', color='orange')

plt.plot(acc_ar, s_eff_diam_ar, label='Effective Diameter', color='g')
plt.axhline(s_ex_eff_dia, linestyle='dashed', color='g')

plt.legend()
title = 'approximation method: sample random pairs of vertices \n approximate network statistics as a function of the accuracy parameter for  the LSCC \n for the network: ' + filenames[0].split('.')[0]
plt.title(title)
plt.xlabel('accuracy[%]')
plt.ylabel('distance')
plt.savefig('./figures/2_2_' + filenames[0].split('.')[0] + '_lscc', dpi=300, bordes='tight')

plt.figure(figsize=(12,6))
plt.plot(acc_ar, w_median_ar, label='Median distance', color='navy')
plt.axhline(w_ex_median, linestyle='dashed', color='navy')

plt.plot(acc_ar, w_mean_ar, label='Mean distance', color='r')
plt.axhline(w_ex_mean, linestyle='dashed', color='r')

plt.plot(acc_ar, w_diam_ar, label='Diameter', color='orange')
plt.axhline(w_ex_dia, linestyle='dashed', color='orange')

plt.plot(acc_ar, w_eff_diam_ar, label='Effective Diameter', color='g')
plt.axhline(w_ex_eff_dia, linestyle='dashed', color='g')
plt.legend()
title = 'approximation method: sample random pairs of vertices \n approximate network statistics as a function of the accuracy parameter for  the LWCC \n for the network: ' + filenames[0].split('.')[0]
plt.title(title)
plt.xlabel('accuracy[%]')
plt.ylabel('distance')
plt.savefig('./figures/2_2_' + filenames[0].split('.')[0] + '_lwcc', dpi=300, bordes='tight')

print('complete code: \t', int(divmod(time.time() - start, 60)[0]), 'min:', int(divmod(time.time() - start, 60)[1]),'s')
