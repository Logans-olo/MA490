from .block_elim import schur_block
from .block_elim import schur_eliminate_scalar 
import numpy as np
def elimination( matrix: np.ndarray):
    n = matrix.shape[0]

    active = list(range(n))
    schur_terms = []

    while active:
        k = active[0]   

        S = schur_eliminate_scalar(matrix, k)
        schur_terms.append(S)

        active.remove(k)
    return schur_terms