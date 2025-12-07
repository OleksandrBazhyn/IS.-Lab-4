class Sudoku:
    SIZE = 9
    BLOCK_ROWS = 3
    BLOCK_COLS = 3

    def __init__(self, grid):
        self.grid = [[None if v == 0 else v for v in row] for row in grid]

    def get(self, r, c):
        return self.grid[r][c]

    def set(self, r, c, v):
        self.grid[r][c] = v

    def row(self, r):
        return self.grid[r]

    def col(self, c):
        return [self.grid[r][c] for r in range(self.SIZE)]

    def block(self, r, c):
        br = (r // self.BLOCK_ROWS) * self.BLOCK_ROWS
        bc = (c // self.BLOCK_COLS) * self.BLOCK_COLS
        return [
            self.grid[i][j]
            for i in range(br, br + self.BLOCK_ROWS)
            for j in range(bc, bc + self.BLOCK_COLS)
        ]

    def valid(self, r, c, v):
        if v is None:
            return True
        if v in self.row(r): return False
        if v in self.col(c): return False
        if v in self.block(r, c): return False
        return True

    def neighbors(self, r, c):
        result = set()
        for i in range(self.SIZE):
            if i != c: result.add((r, i))
            if i != r: result.add((i, c))

        br = (r // self.BLOCK_ROWS) * self.BLOCK_ROWS
        bc = (c // self.BLOCK_COLS) * self.BLOCK_COLS
        for i in range(br, br + self.BLOCK_ROWS):
            for j in range(bc, bc + self.BLOCK_COLS):
                if (i, j) != (r, c):
                    result.add((i, j))

        return list(result)

    def print(self):
        line = "-" * 25
        for r in range(self.SIZE):
            if r % self.BLOCK_ROWS == 0:
                print(line)

            for c in range(self.SIZE):
                if c % self.BLOCK_COLS == 0:
                    print("|", end=" ")

                v = self.grid[r][c]
                print("·" if v is None else v, end=" ")

            print("|")
        print(line)
