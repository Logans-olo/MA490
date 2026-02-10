from matrix_type import generate_matrix
def main():
    print(generate_matrix("band", 10))
    print(generate_matrix("band", 4))
    print(generate_matrix("random", 10))
if __name__ == "__main__":
    main()