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

ring = DecadeRing()

for i in range(10):
    carry = ring.pulse()
    print("Digit:", ring.digit, "| Carry:", carry)