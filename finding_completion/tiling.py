def make_cycle_block(k):
    """Create the adjacency matrix for a cycle of size k,
    with 1 on diagonal and adjacent edges, -1 on the wrap-around edge,
    and None elsewhere."""
    block = [[None] * k for _ in range(k)]
    for i in range(k):
        block[i][i] = 1
        if i + 1 < k:
            block[i][i + 1] = 1
            block[i + 1][i] = 1
    # Wrap-around edge gets -1
    block[0][k - 1] = -1
    block[k - 1][0] = -1
    return block


def tile(cycle_sizes):
    """Build a block-diagonal matrix from a list of cycle sizes.
    
    Args:
        cycle_sizes: list of ints, e.g. [4, 4] or [4, 6, 3]
    
    Returns:
        A square matrix (list of lists) with cycle adjacency blocks
        along the diagonal, 0 off-diagonal, and None for non-edges
        within each block.
    """
    if not cycle_sizes:
        return []

    total = sum(cycle_sizes)
    matrix = [[None] * total for _ in range(total)]

    offset = 0
    for k in cycle_sizes:
        block = make_cycle_block(k)
        for r in range(k):
            for c in range(k):
                matrix[offset + r][offset + c] = block[r][c]
        offset += k

    return matrix


# ---- backward-compatible wrapper ----
def tile_top_left_4x4(n):
    return tile([4] * n)


given_matrix = [
    [1,    1,    None, -1,   None, None, None, None],
    [1,    1,    1,    None, None, None, None, None],
    [None, 1,    1,    1,    None, None, None, None],
    [-1,   None, 1,    1,    None, None, None, None],
    [None, None, None, None, 1,    1,    None, -1],
    [None, None, None, None, 1,    1,    1,    None],
    [None, None, None, None, None, 1,    1,    1],
    [None, None, None, None, -1,   None, 1,    1],
]

if __name__ == "__main__":
    assert given_matrix == tile_top_left_4x4(2)
    print("4x4 x2 passed")

    [print(x) for x in tile([4, 6])]