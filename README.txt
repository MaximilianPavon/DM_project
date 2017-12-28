README file for: Programming project CS-E4600 - Algorithmic Methods of Data Mining

authors: Héctor Laria Mantecón and Maximilian Proll

Packages:

This project has been programmed using Graph-Tool and NetworkX Python libraries.
Data exploration has been performed using Jupyter Notebooks.
Both NetworkX and Jupyter Notebook are common and can be obtained from an Anaconda
installation or installed by PIP. For installing Graph-Tool however, we recommend
using its docker container instead because of the huge amount of dependencies and
the problems installing some of them.
More information here https://git.skewed.de/count0/graph-tool/wikis/installation-instructions#installing-using-docker

Nomenclatura for files:

prefix:
gt_* 			- file written using library graph-tool
nx_*			- file written using library networkX

middlefix:
*_exact_stats_*		- compute exact statistics
*_approx_*		- compute approximate statistics with random sampling of pairs of vertices
*_brute_*		- indicates that this code has been used to run on brute/force

suffix:
indicates which network has been used
*_wiki_*   				- WikiVote network
*_soc-Epinions1_* *_soc_epi_* *_epi_*	- Epinions network

file ending:
*.py			- Python file
*.ipynb			- Jupyter Notebook

analysis.py and analysis_nx.py define functions in Graph-Tool and NetworkX respectively
