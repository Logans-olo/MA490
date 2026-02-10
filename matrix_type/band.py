import numpy as np

def generate_band(n, k=2):
    """
    Generate a symmetric, banded SPD matrix.
    Diagonal dominance guarantees SPD.
    """
    A = np.zeros((n,n))
    
    for i in range(n):
        for j in range(max(0, i-k), min(n, i+k+1)):
            A[i,j] = np.random.rand() + 0.5  # some positive weight
            A[j,i] = A[i,j]  # symmetry
    
    # Diagonal dominance
    for i in range(n):
        A[i,i] += np.sum(np.abs(A[i,:]))  # sum of off-diagonal
    
    return A