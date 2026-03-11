import networkx as nx 
import numpy as np
"""
Very simple set of functions for testing graph products.
These are simply warreprs over Networkx functions
Designed to be used with Numpy Arrays

"""
def cartesian_product(A: np.ndarray, B: np.ndarray):
    G = nx.from_numpy_array(A)
    H = nx.from_numpy_array(B)
    P = nx.cartesian_product(G, H)
    return nx.to_numpy_array(P, dtype=int)

def tensor_product(A: np.ndarray, B: np.ndarray):
    G = nx.from_numpy_array(A)
    H = nx.from_numpy_array(B)
    P = nx.tensor_product(G, H)
    return nx.to_numpy_array(P, weight=None, dtype=int)
