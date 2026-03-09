from utils import clique
from utils import products
import numpy as np
import cvxpy as cp

n = 4
p = 0.3

def run():
    
    A = random_graph(n,p)
    print(np.linalg.eigvals(A))
    B = random_graph(n,p)
    print(np.linalg.eigvals(B))
    P = products.cartesian_product(A, B)
    print(np.linalg.eigvals(P))
    P = products.tensor_product(A, B)
    print(np.linalg.eigvals(P))
def random_graph(n, p):
    M = np.random.rand(n, n) < p
    A = np.triu(M, 1)
    A = A + A.T  # make symmetric (undirected)
    np.fill_diagonal(A, 0)
    return A

if __name__ == "__main__":
    run()