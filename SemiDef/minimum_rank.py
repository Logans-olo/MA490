import numpy as np
from scipy.optimize import minimize
 
 
def _make_loss(edges: set, n: int, r: int):
    """Build loss + analytic gradient over V (n x r) with M = V @ V.T."""
 
    def loss(V_flat):
        V = V_flat.reshape(n, r)
        M = V @ V.T
        val = 0.0
 
        for i in range(n):
            for j in range(i + 1, n):
                m_ij = M[i, j]
                if (i, j) not in edges:
                    val += m_ij ** 2                     # want M_ij = 0
                else:
                    val += max(0.0, 1.0 - m_ij ** 2)    # want |M_ij| >= 1
 
        for i in range(n):
            val += max(0.0, 0.1 - M[i, i]) * 10.0      # keep diagonal > 0
 
        return val
 
    def grad(V_flat):
        V = V_flat.reshape(n, r)
        M = V @ V.T
        dL_dM = np.zeros((n, n))
 
        for i in range(n):
            for j in range(i + 1, n):
                m_ij = M[i, j]
                if (i, j) not in edges:
                    g = 2.0 * m_ij
                else:
                    g = 0.0 if m_ij ** 2 >= 1.0 else -2.0 * m_ij
                dL_dM[i, j] += g
                dL_dM[j, i] += g
 
        for i in range(n):
            if M[i, i] < 0.1:
                dL_dM[i, i] -= 10.0
 
        return (2.0 * dL_dM @ V).ravel()
 
    return loss, grad
 
 
def min_rank_exact(
    edge_set,
    n: int,
    max_rank: int = None,
    restarts: int = 100,
    tol: float = 1e-4,
) -> dict:
    """
    Find minimum rank by trying r = 1, 2, ..., max_rank.
    Returns as soon as a feasible solution is found.
    """
    if max_rank is None:
        max_rank = n
 
    edges = set(edge_set) | {(j, i) for (i, j) in edge_set}
 
    best_loss = float("inf")
 
    for r in range(1, max_rank + 1):
        loss_fn, grad_fn = _make_loss(edges, n, r)
        best_r_loss = float("inf")
        best_V = None
 
        for _ in range(restarts):
            V0 = np.random.randn(n * r) / np.sqrt(r)
            res = minimize(
                loss_fn,
                V0,
                jac=grad_fn,
                method="L-BFGS-B",
                options={"maxiter": 2000, "ftol": 1e-14, "gtol": 1e-8},
            )
            if res.fun < best_r_loss:
                best_r_loss = res.fun
                best_V = res.x.reshape(n, r)
            if best_r_loss < tol:
                break
 
        best_loss = best_r_loss
 
        if best_r_loss < tol:
            M = best_V @ best_V.T
            eigvals = np.linalg.eigvalsh(M)
            rank = int(np.sum(eigvals > 1e-6))
            return {
                "minimum_rank": rank,
                "matrix": M,
                "eigenvalues": eigvals,
                "success": True,
                "loss": best_r_loss,
            }
 
    return {
        "minimum_rank": max_rank,
        "matrix": None,
        "eigenvalues": None,
        "success": False,
        "loss": best_loss,
    }
 
 
def minimum_rank(edge_set: set, n: int, method: str = "sdp", **kwargs) -> dict:
    """Unified interface — method name kept for compatibility."""
    if method in ("sdp", "exact", "random"):
        return min_rank_exact(edge_set, n, **kwargs)
    raise ValueError(f"Unknown method '{method}'.")
 
 
if __name__ == "__main__":
    tests = [
        ("P4",   4, {(0,1),(1,2),(2,3)}),
        ("K3",   3, {(0,1),(1,2),(0,2)}),
        ("Star", 4, {(0,1),(0,2),(0,3)}),
        ("C4",   4, {(0,1),(1,2),(2,3),(3,0)}),
        ("K4",   4, {(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)}),
    ]
 
    print(f"{'Graph':<10} {'n':>3} {'mr':>5} {'loss':>12} {'ok?':>5}")
    print("-" * 40)
    for name, n, edges in tests:
        result = minimum_rank(edges, n)
        ok = "YES" if result["success"] else "NO"
        print(f"{name:<10} {n:>3} {result['minimum_rank']:>5} "
              f"{result['loss']:>12.2e} {ok:>5}")