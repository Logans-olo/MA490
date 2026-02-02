import sys
import numpy as np
def init(): 

    n = int(sys.argv[1])
    k = int(sys.argv[2])

    if (n < k): 
        print("Bandwidth cannot be larger than Matrix")
        exit(2)
    matrix = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            if( (j < i - k) or (j > i + k)): 
                matrix[i][j] = 0
            else:
                matrix[i][j] = 1
    matrix += np.eye(n) * 1
    return matrix

def decomp(matrix):
    """This function takes a 2 x 2 matrix and decomposes it such that the first off-diagonal is removed
    This is done via a replacement with the Schur componenet

    Args:
        matrix (int): A 2x2 matrix that should be dense.
    """
    k = 2

    A  = matrix[0:k, 0:k]
    D  = matrix[0:k, k:2*k]
    Dt = matrix[k:2*k, 0:k]
    B  = matrix[k:2*k, k:2*k]
    X = np.linalg.solve(A, D)
    B = B - Dt @ X
    matrix[0:k, 0:k] = A
    matrix[0:k, k:2*k] = 0
    matrix[k:2*k, 0:k] = 0
    matrix[k:2*k, k:2*k] = B
    # print(matrix)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Provide a Matrix Size, and a bandwidth constants")
        exit(1)
    matrix = init()
    # print(matrix)
    decomp(matrix)
