import networkx as nx
import numpy as np

def max_cliques(A: np.array):
    G = nx.from_numpy_array(A)
    cliques = list(nx.find_cliques(G))
    return cliques
    
    