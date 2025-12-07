from variable import Variable

class CspSolver:
    def __init__(self, sudoku, mrv=True, degree=True, lcv=True):
        self.sudoku = sudoku
        self.vars = []
        self.mrv = mrv
        self.degree = degree
        self.lcv = lcv
        self.backtracks = 0
        self.init_vars()

    def init_vars(self):
        for r in range(self.sudoku.SIZE):
            for c in range(self.sudoku.SIZE):
                v = self.sudoku.get(r, c)
                var = Variable(r, c, v)

                if v is None:
                    var.domain = [
                        i for i in range(1, 10)
                        if self.sudoku.valid(r, c, i)
                    ]

                self.vars.append(var)

    def solve(self):
        return self.backtrack()

    def backtrack(self):
        var = self.select_var()
        if not var:
            return True

        values = self.order_values(var)
        for v in values:
            if self.sudoku.valid(var.r, var.c, v):
                var.value = v
                self.sudoku.set(var.r, var.c, v)

                saved = {x: x.domain[:] for x in self.vars if not x.assigned}
                self.forward_check(var)

                if self.backtrack():
                    return True

                self.backtracks += 1
                var.value = None
                self.sudoku.set(var.r, var.c, None)

                for k in saved:
                    k.domain = saved[k]

        return False

    def select_var(self):
        unassigned = [v for v in self.vars if not v.assigned]
        if not unassigned:
            return None

        if self.mrv:
            minimum = min(len(v.domain) for v in unassigned)
            candidates = [v for v in unassigned if len(v.domain) == minimum]
            if self.degree:
                return max(candidates, key=self.degree_count)
            return candidates[0]

        if self.degree:
            return max(unassigned, key=self.degree_count)

        return unassigned[0]

    def degree_count(self, var):
        return sum(
            1 for (r, c) in self.sudoku.neighbors(var.r, var.c)
            if self.find_var(r, c) and not self.find_var(r, c).assigned
        )

    def find_var(self, r, c):
        return next((v for v in self.vars if v.r == r and v.c == c), None)

    def order_values(self, var):
        if not self.lcv:
            return var.domain
        return sorted(var.domain, key=lambda v: self.value_cost(var, v))

    def value_cost(self, var, val):
        cost = 0
        for (r, c) in self.sudoku.neighbors(var.r, var.c):
            nbr = self.find_var(r, c)
            if nbr and not nbr.assigned and val in nbr.domain:
                cost += 1
        return cost

    def forward_check(self, var):
        for (r, c) in self.sudoku.neighbors(var.r, var.c):
            nbr = self.find_var(r, c)
            if nbr and not nbr.assigned and var.value in nbr.domain:
                nbr.domain.remove(var.value)
