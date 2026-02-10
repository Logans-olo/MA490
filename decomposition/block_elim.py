
import numpy as np
def schur_eliminate_scalar(matrix, k):
    """
    Eliminates index k from an SPD matrix using a numerically
    stable scalar Schur complement.

    Returns
    -------
    S : np.ndarray
        PSD Schur complement contribution (same size as matrix)
    """

    n = matrix.shape[0]

    a = matrix[k, k]
    if a <= 0:
        raise ValueError("Pivot is not positive — matrix not SPD under this ordering.")

    # Indices of remaining variables
    idx = [i for i in range(n) if i != k]

    d = matrix[k, idx]
    s = d / np.sqrt(a)

    # Local PSD contribution
    S_local = np.outer(s, s)

    S = np.zeros_like(matrix)
    for i, ii in enumerate(idx):
        for j, jj in enumerate(idx):
            S[ii, jj] = S_local[i, j]

    matrix[np.ix_(idx, idx)] -= S_local

    matrix[k, :] = 0.0
    matrix[:, k] = 0.0
    matrix[k, k] = a 

    return S


def schur_block(matrix, i0, i1, i2):
    """
    Block Schur complement elimination using a numerically stable
    Cholesky-based formulation.

    Eliminates block [i0:i1] and updates block [i1:i2].

    Parameters
    ----------
    matrix : np.ndarray
        Symmetric positive definite matrix (modified in place)
    i0, i1, i2 : int
        Block indices
    """

    # Extract blocks
    A  = matrix[i0:i1, i0:i1]      # eliminated block (SPD)
    D  = matrix[i0:i1, i1:i2]      # coupling block
    Dt = matrix[i1:i2, i0:i1]      # transpose
    B  = matrix[i1:i2, i1:i2]      # trailing block

    # A = L L^T
    L = np.linalg.cholesky(A)
    Y = np.linalg.solve(L, D)

    # Schur complement contribution (PSD)
    S = Y.T @ Y
    B_new = B - S
    
    matrix[i1:i2, i1:i2] = B_new
    D = 0.0
    Dt = 0.0 #dt

    return S