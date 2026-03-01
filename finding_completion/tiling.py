def tile_top_left_4x4(n):
    if n <= 0:
        return []
    
    block = [
        [ 1,  1, None, -1],
        [ 1,  1,  1,  None],
        [None,  1,  1,   1 ],
        [-1, None,  1,   1 ]
    ]
    
    size = 4 * n
    return [
        [
            block[r % 4][c % 4] if (r // 4 == c // 4) else 0
            for c in range(size)
        ]
        for r in range(size)
    ]
given_matrix = [
    [1,    1,    None, -1,    None, None, None, None],
    [1,    1,    1,   None, None, None, None,    None],
    [None, 1,   1,    1,    None, None,  None, None],
    [-1,    None, 1,    1,    None,    None, None, None],
    [None, None, None, None,    1,    1,   None, -1],
    [None, None, None,    None, 1,   1,    1,    None],
    [None, None,    None, None, None, 1,    1,    1],
    [None,   None, None, None, -1,    None, 1,    1]
]
if __name__ == "__main__":
    print(given_matrix == tile_top_left_4x4(2))
    [print(x) for x in tile_top_left_4x4(3)]
