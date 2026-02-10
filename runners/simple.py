from matrix_type import generate_matrix
from decomposition import elimination
def main():
    A = generate_matrix("band", 10)
    print(elimination(A))
    print(A)
    #dual_elimination(generate_matrix("band", 4))
    #dual_elimination(generate_matrix("random", 10))
if __name__ == "__main__":
    main()