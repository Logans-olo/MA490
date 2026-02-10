import numpy as np

def factor_sum(L):
    A = np.zeros_like(L[0])
    for P in L:
        A += P
    return A