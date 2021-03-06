import numbers


class FieldInt(object):
    """A non-negative integer modulo a prime number."""

    # -- Instance management methods --

    # The modulus must be prime, which is not checked!
    def __init__(self, value, modulus):
        if not isinstance(value, numbers.Integral) or not isinstance(modulus, numbers.Integral):
            raise TypeError("Expected integers")
        if modulus <= 0:
            raise ValueError("Modulus must be positive")
        if not (0 <= value < modulus):
            raise ValueError("Value out of range")
        self.value = value
        self.modulus = modulus

    def _create(self, val):
        return FieldInt(val % self.modulus, self.modulus)

    def _check(self, other):
        if not isinstance(other, FieldInt):
            raise TypeError("Expected FieldInt")
        if self.modulus != other.modulus:
            raise ValueError("Other number must have same modulus")

    # -- Arithmetic methods --

    def __add__(self, other):
        self._check(other)
        return self._create(self.value + other.value)

    def __sub__(self, other):
        self._check(other)
        return self._create(self.value - other.value)

    def __neg__(self):
        return self._create(-self.value)

    def __mul__(self, other):
        self._check(other)
        return self._create(self.value * other.value)

    def reciprocal(self):
        if self.value == 0:
            raise ValueError("Division by zero")
        # Extended Euclidean algorithm
        x, y = self.modulus, self.value
        a, b = 0, 1
        while y != 0:
            a, b = b, a - x // y * b
            x, y = y, x % y
        if x == 1:
            return self._create(a)
        else:
            raise ValueError("Value and modulus not coprime")

    # -- Comparison methods --

    def __eq__(self, other):
        return isinstance(other, FieldInt) and (self.value, self.modulus) == (other.value, other.modulus)

    def __ne__(self, other):
        return not (self == other)

    # -- Miscellaneous methods --

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "FieldInt(value={}, modulus={})".format(self.value, self.modulus)
