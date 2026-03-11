from utils import clique
from utils import products
import numpy as np
import cvxpy as cp


    
def random_graph(n, p):
    M = np.random.rand(n, n) < p
    A = np.triu(M, 1)
    A = A + A.T  # make symmetric (undirected)
    np.fill_diagonal(A, 0)
    return A

def experiment(num_trials=100, n=3, p=0.5):

    ranks = []

    for _ in range(num_trials):

        A = random_graph(n, p)

        rank, eigvals = psd_completion_rank(A)

        if rank is not None:
            ranks.append(rank)

    print("Trials:", num_trials)
    print("Average rank:", np.mean(ranks))
    print("Max rank:", np.max(ranks))
    print("Min rank:", np.min(ranks))

def psd_completion_rank(A_G):

    n = A_G.shape[0]

    for k in range(1, n+1):

        Y = cp.Variable((n,n), symmetric=True)

        constraints = [Y >> 0, cp.trace(Y) <= k]

        for i in range(n):
            for j in range(n):
                if A_G[i,j] != 0:
                    constraints.append(Y[i,j] == A_G[i,j])

        prob = cp.Problem(cp.Minimize(cp.Trace(Y)), constraints)
        prob.solve(solver=cp.SCS, verbose=False)

        if prob.status == "optimal":

            eigvals = np.linalg.eigvalsh(Y.value)
            rank = np.sum(eigvals > 1e-6)

            return rank, eigvals
    return None, None
def product_experiment(num_trials=50, n=3, p=0.5):

    rank_A = []
    rank_B = []
    rank_cart = []
    rank_tensor = []

    for _ in range(num_trials):

        A = random_graph(n, p)
        B = random_graph(n, p)

        rA, _ = psd_completion_rank(A)
        rB, _ = psd_completion_rank(B)

        P_cart = products.cartesian_product(A, B)
        P_tensor = products.tensor_product(A, B)

        r_cart, _ = psd_completion_rank(P_cart)
        r_tensor, _ = psd_completion_rank(P_tensor)

        if None not in (rA, rB, r_cart, r_tensor):
            rank_A.append(rA)
            rank_B.append(rB)
            rank_cart.append(r_cart)
            rank_tensor.append(r_tensor)
            print(r_cart, rA, rB)

    print("Trials:", num_trials)

    print("\nAverage ranks")
    print("A:", np.mean(rank_A))
    print("B:", np.mean(rank_B))
    print("Cartesian:", np.mean(rank_cart))
    print("Tensor:", np.mean(rank_tensor))

    print("\nMax ranks")
    print("A:", np.max(rank_A))
    print("B:", np.max(rank_B))
    print("Cartesian:", np.max(rank_cart))
    print("Tensor:", np.max(rank_tensor))
    return None, None
if __name__ == "__main__":
    experiment()
    product_experiment()