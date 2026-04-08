import argparse
import numpy as np
import networkx as nx
 
from completion_number import completion_number
from minimum_rank import minimum_rank
 
 
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def graph_to_partial_matrix(G_nx: nx.Graph, n: int) -> np.ndarray:
    """
    Convert a networkx graph to a partial positive matrix A_G.
 
    Specified entries:
        - Diagonal: all set to n (large enough to keep matrix positive)
        - Off-diagonal (i,j) in E: set to a small fixed positive value
          so the matrix remains positive on specified entries.
    Free entries: off-diagonal (i,j) not in E, left as 0 (marker for free).
    """
    A = np.zeros((n, n))
    np.fill_diagonal(A, float(n))  # large positive diagonal
 
    for (i, j) in G_nx.edges():
        # Small off-diagonal entry; keep |a_ij| < sqrt(a_ii * a_jj) for
        # the specified submatrix to be positive definite
        val = 0.5
        A[i, j] = val
        A[j, i] = val
 
    return A
 
 
def graph_to_edge_set(G_nx: nx.Graph) -> set:
    edges = set()
    for (i, j) in G_nx.edges():
        edges.add((i, j))
        edges.add((j, i))
    return edges
 
 
# ---------------------------------------------------------------------------
# Single trial
# ---------------------------------------------------------------------------
 
def run_trial(n: int, edge_prob: float = 0.5) -> dict:
    """
    Generate a random graph, compute mr(G) and c(G), check conjecture.
    """
    G_nx = nx.gnp_random_graph(n, edge_prob)
    edges = graph_to_edge_set(G_nx)
    A_G   = graph_to_partial_matrix(G_nx, n)
 
    cn_result = completion_number(A_G)
    mr_result = minimum_rank(edges, n, method="sdp")
 
    cn = cn_result["completion_number"]
    mr = mr_result["minimum_rank"]
 
    diff = (mr - cn) if (mr is not None and cn is not None) else None
    conjecture_holds = (diff == 1) if diff is not None else None
 
    return {
        "n": n,
        "num_edges": G_nx.number_of_edges(),
        "edges": list(G_nx.edges()),
        "cn": cn,
        "mr": mr,
        "diff": diff,
        "conjecture_holds": conjecture_holds,
        "cn_eigenvalues": cn_result["eigenvalues"],
        "cn_negative_inertia": cn_result["negative_inertia"],
    }
 
 
# ---------------------------------------------------------------------------
# Batch test
# ---------------------------------------------------------------------------
 
def test_conjecture(
    n: int = 4,
    num_trials: int = 100,
    edge_prob: float = 0.5,
    verbose: bool = True,
) -> list:
    """
    Run num_trials random graphs of size n and test mr(G) = c(G) + 1.
    """
    results = []
    holds_count = 0
    fail_count  = 0
    error_count = 0
 
    print(f"Testing conjecture mr(G) = c(G) + 1")
    print(f"n={n}, trials={num_trials}, edge_prob={edge_prob}")
    print("-" * 60)
    print(f"{'Trial':>6}  {'edges':>5}  {'mr':>4}  {'c(G)':>5}  {'diff':>5}  {'holds?':>8}")
    print("-" * 60)
 
    for trial in range(1, num_trials + 1):
        r = run_trial(n, edge_prob)
        results.append(r)
 
        if r["conjecture_holds"] is None:
            status = "ERROR"
            error_count += 1
        elif r["conjecture_holds"]:
            status = "YES"
            holds_count += 1
        else:
            status = f"NO  <-- diff={r['diff']}"
            fail_count += 1
 
        if verbose:
            print(
                f"{trial:>6}  {r['num_edges']:>5}  "
                f"{str(r['mr']):>4}  {str(r['cn']):>5}  "
                f"{str(r['diff']):>5}  {status}"
            )
 
    print("-" * 60)
    print(f"Conjecture HOLDS : {holds_count}/{num_trials}")
    print(f"Conjecture FAILS : {fail_count}/{num_trials}")
    print(f"Errors           : {error_count}/{num_trials}")
 
    counterexamples = [r for r in results if r["conjecture_holds"] is False]
    if counterexamples:
        print()
        print("=== COUNTEREXAMPLES ===")
        for r in counterexamples:
            print(f"  Edges: {r['edges']}")
            print(f"  mr={r['mr']}, c(G)={r['cn']}, diff={r['diff']}")
            print(f"  Eigenvalues of completion: {np.round(r['cn_eigenvalues'], 4)}")
            print()
    else:
        print()
        print("No counterexamples found.")
 
    return results
 
 
# ---------------------------------------------------------------------------
# Sweep over n
# ---------------------------------------------------------------------------
 
def sweep_n(
    n_values: list = None,
    trials_per_n: int = 50,
) -> None:
    """
    Test the conjecture across multiple values of n.
    """
    if n_values is None:
        n_values = [3, 4, 5, 6]
 
    print("=== Sweep over graph sizes ===")
    print(f"{'n':>3}  {'holds':>6}  {'fails':>6}  {'errors':>7}")
    print("-" * 30)
 
    for n in n_values:
        results = test_conjecture(n=n, num_trials=trials_per_n, verbose=False)
        holds  = sum(1 for r in results if r["conjecture_holds"] is True)
        fails  = sum(1 for r in results if r["conjecture_holds"] is False)
        errors = sum(1 for r in results if r["conjecture_holds"] is None)
        print(f"{n:>3}  {holds:>6}  {fails:>6}  {errors:>7}")
 
    print()
 
 
# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test conjecture mr(G) = c(G) + 1")
    parser.add_argument("--n",      type=int,   default=4,    help="Graph size")
    parser.add_argument("--trials", type=int,   default=50,   help="Number of random graphs")
    parser.add_argument("--prob",   type=float, default=0.5,  help="Edge probability")
    parser.add_argument("--sweep",  action="store_true",      help="Sweep over n=3..6")
    args = parser.parse_args()

    if args.sweep:
        sweep_n(n_values=[3, 4, 5, 6], trials_per_n=args.trials)
    else:
        test_conjecture(n=args.n, num_trials=args.trials, edge_prob=args.prob)