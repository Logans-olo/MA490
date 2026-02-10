
def decomp(matrix, i0, i1, i2):
    """This function takes a 2 x 2 matrix and decomposes it such that the first off-diagonal is removed
    This is done via a replacement with the Schur componenet

    Args:
        matrix (int): A 2x2 matrix that should be dense.
    """
    

    A  = matrix[i0:i1, i0:i1]
    D  = matrix[i0:i1, i1:i2]
    Dt = matrix[i1:i2, i0:i1]
    B  = matrix[i1:i2,  i1:i2]
    X = np.linalg.solve(A, D)
    B = B - Dt @ X
    matrix[i1:i2, i1:i2] = B
    matrix[i0:i1, i1:i2] = 0
    matrix[i1:i2, i0:i1] = 0