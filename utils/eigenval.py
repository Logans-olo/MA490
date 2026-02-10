import numpy as np
def eigen_summary(matrix: np.ndarray, tol: float = 1e-12) -> dict:
    eigvals = np.linalg.eigvalsh(matrix)
    return {
        "positive": np.sum(eigvals > tol),
        "negative": np.sum(eigvals < -tol),
        "near_zero": np.sum(np.abs(eigvals) <= tol),
    }