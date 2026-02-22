from .eigenval import eigen_summary
from .factor_sum import factor_sum
from .clique import max_cliques
import numpy as np
def report(psd_terms, A_original, tol = 1e-12):
    A_sum = np.zeros_like(A_original)

    for i, S in enumerate(psd_terms):
        nz = np.where(np.abs(S) > tol)
        support = sorted(set(nz[0]).union(nz[1]))

        print(f"\n--- Term {i} ---")
        print(f"Support (clique): {support}")
        print("PSD term S_i:")
        print(S)

        eigvals = np.linalg.eigvalsh(S)
        print("Eigenvalues:", np.round(eigvals, 6))

        A_sum += S

    print("\n--- Reconstruction check ---")
    print("Sum of terms:")
    print(A_sum)

    err = np.linalg.norm(A_sum - A_original)
    print("||A - sum S_i|| =", err)