class DecadeRing:
    def __init__(self):
        self.s = [0] * 10   # one-hot stages
        self.clear()

    def clear(self):
        self.s = [0] * 10
        self.s[0] = 1       # stage 0 triggered, others normal

    @property
    def digit(self):
        return self.s.index(1)

    def pulse(self):
        d = self.digit
        self.s[d] = 0
        self.s[(d + 1) % 10] = 1
        return d == 9       # carry out when wrapping 9 -> 0


class Accumulator:
    N = 10

    def __init__(self):
        self.d = [DecadeRing() for _ in range(self.N)]   # d[0] = units
        self.sign = 'P'

    def clear(self):
        for r in self.d:
            r.clear()
        self.sign = 'P'

    def _toggle(self):
        self.sign = 'M' if self.sign == 'P' else 'P'

    def _receive(self, pulses):
        # pulses[i] = number of digit pulses arriving at decade i
        carries = [0] * (self.N + 1)
        for i in range(self.N):
            for _ in range(pulses[i] + carries[i]):
                if self.d[i].pulse():            # wrapped 9 -> 0
                    carries[i + 1] += 1
        if carries[self.N]:                       # carry out of the top decade
            self._toggle()

    def _digits(self, x):
        n = x if x >= 0 else 10**self.N + x       # 10's complement for negatives
        return [(n // 10**i) % 10 for i in range(self.N)]

    def add(self, x):                             # channel A
        self._receive(self._digits(x))
        if x < 0:
            self._toggle()                        # an M sign toggles the sign counter

    def subtract(self, x):                        # channel S
        nines = [9 - dg for dg in self._digits(x)]
        nines[0] += 1                             # the Integral Pulse (the +1)
        self._receive(nines)
        if x >= 0:
            self._toggle()                        # S sends the opposite sign

    def value(self):
        n = sum(r.digit * 10**i for i, r in enumerate(self.d))
        return n if self.sign == 'P' else n - 10**self.N

a = Accumulator(); a.add(5); a.subtract(2); print(a.value())    # 3
a.clear(); a.add(3); a.subtract(7); print(a.value())            # -4
a.clear(); a.add(-46); a.add(50); print(a.value())              # 4