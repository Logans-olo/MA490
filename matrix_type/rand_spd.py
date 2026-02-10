import numpy as np
import random 

def generate_rand_spd(n):
    
    A = np.random.rand(n,n) 
    matrix = .5 * np.dot(A, A.transpose())
    return matrix