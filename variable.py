class Variable:
    def __init__(self, r, c, value=None):
        self.r = r
        self.c = c
        self.value = value
        self.domain = []

    @property
    def assigned(self):
        return self.value is not None
