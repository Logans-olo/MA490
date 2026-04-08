from completion_number import completion_number
from minimum_rank import minimum_rank
import numpy as np

tests = [
    ("P4",   4, {(0,1),(1,2),(2,3)}),
    ("K3",   3, {(0,1),(1,2),(0,2)}),
    ("Star", 4, {(0,1),(0,2),(0,3)}),
    ("C4",   4, {(0,1),(1,2),(2,3),(3,0)}),
    ("K4",   4, {(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)}),
    ("C5", 5, {(0,1), (1,2), (2,3), (3,4), (4,0)}),
    
]

for name, n, edges in tests:
    A = np.full((n, n), np.nan)
    np.fill_diagonal(A, 1.0)
    for (i,j) in edges:
        A[i,j] = 0.5
        A[j,i] = 0.5

    cn = completion_number(A)["completion_number"]
    mr = minimum_rank(edges, n)["minimum_rank"]
    print(f"{name:<6} mr={mr}  c(G)={cn}  diff={mr-cn}")