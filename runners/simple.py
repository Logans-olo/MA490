from matrix_type import generate_matrix
from decomposition import elimination
import copy
from utils import report
def main():
    A_orig = generate_matrix("band", 10)
    A = copy.deepcopy(A_orig)
    print(report(elimination(A), A_orig))
    #print(A)
    #dual_elimination(generate_matrix("band", 4))
    #dual_elimination(generate_matrix("random", 10))
if __name__ == "__main__":
    main()