import numpy as np
from scipy.optimize import differential_evolution
import itertools

from tiling import tile_top_left_4x4
# Original matrix with asymmetry noted
given_matrix = tile_top_left_4x4(1)
MATRIX_SIZE = 4
def solve_symmetric_matrix():
    
    # Find parameters to optimize
    positions = []
    param_idx = {}
    next_param = 0
    
    for i in range(MATRIX_SIZE):
        for j in range(i, MATRIX_SIZE):
            val_ij = given_matrix[i][j]
            val_ji = given_matrix[j][i]
            
            if val_ij is None:
                if (i, j) not in param_idx:
                    positions.append((i, j))
                    param_idx[(i, j)] = next_param
                    if i != j:
                        param_idx[(j, i)] = next_param
                    next_param += 1
    
    def create_matrix(values):
        matrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=float)
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if given_matrix[i][j] is not None:
                    matrix[i][j] = float(given_matrix[i][j])
        
        for (i, j) in positions:
            idx = param_idx[(i, j)]
            matrix[i][j] = values[idx]
            matrix[j][i] = values[idx]
        
        return matrix
    
    def count_negative(values):
        matrix = create_matrix(values)
        eigenvalues = np.linalg.eigvalsh(matrix)
        return np.sum(eigenvalues < -1e-10)
    
    def objective(values):
        matrix = create_matrix(values)
        eigenvalues = np.linalg.eigvalsh(matrix)
        num_negative = np.sum(eigenvalues < -1e-10)
        
        # MINIMIZE negative eigenvalues (changed from maximize)
        obj = num_negative * 100
        negative_eigs = eigenvalues[eigenvalues < -1e-10]
        if len(negative_eigs) > 0:
            obj += np.sum(abs((negative_eigs)) ** 0.5) * 0.01  # Penalize more negative values
        
        return obj
    
    num_params = len(positions)
    
    # Quick integer search
    best_int_count = 0
    best_int_sol = None
    
    for _ in range(10000):
        values = np.random.randint(-5, 6, num_params).astype(float)
        count = count_negative(values)
        if count > best_int_count:
            best_int_count = count
            best_int_sol = values.copy()
        if (_ % 100) == 0:
            print("On attempt " + str(_))
    
    # Continuous optimization
    bounds = [(-15, 15)] * num_params
    result = differential_evolution(objective, bounds, seed=42, maxiter=500,
                                    popsize=15, workers=1)
    
    opt_count = count_negative(result.x)
    rounded_count = count_negative(np.round(result.x))
    
    best_count = min(best_int_count, opt_count, rounded_count)
    if best_count == opt_count:
        best_sol = result.x
    elif best_count == rounded_count:
        best_sol = np.round(result.x)
    else:
        best_sol = best_int_sol
    
    final_matrix = create_matrix(best_sol)
    final_eigs = np.linalg.eigvalsh(final_matrix)
    
    return best_count, best_sol, final_matrix, final_eigs, positions, param_idx

# Solve the optimization problem
print("Optimizing symmetric matrix with (1,2) = (2,1) = -1")
print("="*60)
count, sol, mat, eigs, positions, pidx = solve_symmetric_matrix()
print(f"Result: {count} negative eigenvalues")
print(f"Eigenvalues: {np.sort(eigs)}")

print("\n" + "="*60)
print("FINAL SOLUTION")
print("="*60)

print(f"Minimum negative eigenvalues: {count}")
final_mat = mat
final_eigs = eigs
final_sol = sol

print(f"\nIs matrix symmetric? {np.allclose(final_mat, final_mat.T)}")

print("\nEigenvalues:")
for i, eig in enumerate(np.sort(final_eigs)):
    sign = "NEGATIVE" if eig < -1e-10 else ("ZERO" if abs(eig) < 1e-10 else "POSITIVE")
    print(f"  λ_{i+1} = {eig:12.6f}  ({sign})")

# Get eigenvectors
eigenvalues, eigenvectors = np.linalg.eigh(final_mat)
sort_idx = np.argsort(eigenvalues)
eigenvalues = eigenvalues[sort_idx]
eigenvectors = eigenvectors[:, sort_idx]

print("\nEigenvectors:")
for i in range(MATRIX_SIZE):
    print(f"\nEigenvector for λ_{i+1} = {eigenvalues[i]:.6f}:")
    print(f"  {eigenvectors[:, i]}")

print("\nFinal symmetric matrix:")
np.set_printoptions(precision=1, suppress=True, linewidth=120)
print(final_mat)

print("\nParameter values for question marks:")
for i, pos in enumerate(positions):
    print(f"  Position {pos}: {final_sol[i]:.2f}")