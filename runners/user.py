import numpy as np
import copy
from decomposition import elimination
from matrix_type import generate_matrix
from utils import report
def main():
    
    tokens = input("Enter your matrix: ").split("--")
    A_orig = generate_matrix("user", -1, tokens)
    A = copy.deepcopy(A_orig)
    print(report(elimination(A), A_orig))
    print(A)
if __name__ == "__main__": 
    main()