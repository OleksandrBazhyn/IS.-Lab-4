import random

SIZE = 9
BLOCK_ROWS = 3
BLOCK_COLS = 3

def generate(cells_to_remove: int):
    grid = [[0]*SIZE for _ in range(SIZE)]
    fill(grid, 0, 0)
    remove(grid, cells_to_remove)
    return grid

def fill(grid, r, c):
    if c == SIZE:
        return fill(grid, r + 1, 0)
    if r == SIZE:
        return True

    nums = list(range(1, SIZE + 1))
    random.shuffle(nums)

    for v in nums:
        if valid(grid, r, c, v):
            grid[r][c] = v
            if fill(grid, r, c + 1):
                return True
            grid[r][c] = 0

    return False

def valid(grid, r, c, v):
    if v in grid[r]:
        return False

    if v in [grid[i][c] for i in range(SIZE)]:
        return False

    br = (r // BLOCK_ROWS) * BLOCK_ROWS
    bc = (c // BLOCK_COLS) * BLOCK_COLS

    for i in range(br, br + BLOCK_ROWS):
        for j in range(bc, bc + BLOCK_COLS):
            if grid[i][j] == v:
                return False

    return True

def remove(grid, k):
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)

    for i in range(min(k, len(cells))):
        r, c = cells[i]
        grid[r][c] = 0
