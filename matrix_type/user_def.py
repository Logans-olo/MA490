
import numpy as np
def generate_user(tokens):
    n = len(tokens)
    m = len(tokens[0].split("&"))
    print(m)
    A = np.zeros((n,m))
    i = 0
    for row in tokens:
        j = 0 
        columns = row.split("&")
        for value in columns:
            A[i][j] = value
            j = j + 1
        i = i + 1
    return A