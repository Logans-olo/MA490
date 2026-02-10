import numpy as np
import random
def generate_band(n):
    k = 2 #random.randint(0,2)
    matrix = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            if( (j < i - k) or (j > i + k)): 
                matrix[i][j] = 0
            else:
                matrix[i][j] = random.randint(1, 10)
                
    return matrix