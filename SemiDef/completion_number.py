import numpy as np
import cvxpy as cp

def completion_number(A_G: np.ndarray):
    n = A_G.shape[0]

    P = cp.Variable((n, n), hermitian=True)
    N = cp.Variable((n, n), hermitian=True)

    Y = P - N

    constraints = [
        P >> 0,
        N >> 0,
    ]

    mask = ~np.isnan(A_G)
    for i in range(n):
        for j in range(n):
            if mask[i, j]:
                constraints.append(Y[i, j] == A_G[i, j])

    prob = cp.Problem(cp.Minimize(cp.real(cp.trace(N))), constraints)
    prob.solve(solver=cp.SCS)

    Y_val = Y.value
    eigvals = np.linalg.eigvalsh(Y_val)

    tol = 1e-5
    i_minus = int(np.sum(eigvals < -tol))
    i_plus  = int(np.sum(eigvals >  tol))
    rank    = i_minus + i_plus

    return {
        "completion_number": i_minus,
        "negative_inertia": i_minus,
        "positive_inertia": i_plus,
        "rank": rank,
        "eigenvalues": eigvals,
        "solution": Y_val,
        "negative_trace": float(np.real(np.trace(N.value))),
    }


if __name__ == "__main__":
    A_G = np.array([
        [1.0, 1.0, np.nan],
        [np.nan, 1.0, 1.0],
        [-1, 1.0, 1.0],
    ], dtype=float)

    result = completion_number(A_G)

    print(f"Completion number : {result['completion_number']}")
    print(f"Negative inertia  : {result['negative_inertia']}")
    print(f"Positive inertia  : {result['positive_inertia']}")
    print(f"Rank              : {result['rank']}")
    print(f"Eigenvalues       : {result['eigenvalues']}")