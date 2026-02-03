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
    # print(matrix)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Provide a Matrix Size, and a bandwidth constants")
        exit(1)
    matrix = init()
    n = matrix.shape[0]
    # print(matrix)
    k = 2
    for i in range(0, n-k, k): 
        i0 = i
        i1 = i + k
        i2 = i + 2 * k
        decomp(matrix, i0,i1,i2)
        
    print(matrix)
