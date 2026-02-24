import networkx as nx
import numpy as np

def max_cliques(A: np.array):
    G = nx.from_numpy_array(A)
    cliques = list(nx.find_cliques(G))
    return cliques
    
def generate_AG(n_vertices, maximal_cliques):
    """
    Parameters
    ----------
    n_vertices : int
        Number of vertices in the graph (vertices labeled 0,...,n-1)

    maximal_cliques : list of lists
        Each element is a list of vertices forming a maximal clique

    Returns
    -------
    A_G : numpy.ndarray
        The matrix described in the problem
    """

    # Step 1: Compute largest clique size for each vertex
    largest_clique_size = np.zeros(n_vertices, dtype=int)

    for clique in maximal_cliques:
        size = len(clique)
        for v in clique:
            largest_clique_size[v] = max(largest_clique_size[v], size)

    # Step 2: Initialize matrix
    A_G = np.zeros((n_vertices, n_vertices))

    # Step 3: Fill diagonal with 1
    np.fill_diagonal(A_G, 1.0)

    for clique in maximal_cliques:
        for i in clique:
            for j in clique:
                if i != j:
                    n_i = largest_clique_size[i]
                    if n_i > 1:
                        A_G[i, j] = min(1.0/(largest_clique_size[i]-1), 1.0/(largest_clique_size[j]-1))

    return A_G