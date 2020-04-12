

class Calculation():

    def constrain(self, n, low, high):
        return max(min(n,high), low)

    def map(self, n, from1, from2, to1, to2):
        val = (n - from1) / (from2 - from1) * (to2 - to1) + to1
        if to1 < to2:
            return self.constrain(self, val, to1, to2)
        else:
            return self.constrain(self, val, to2,to1)
