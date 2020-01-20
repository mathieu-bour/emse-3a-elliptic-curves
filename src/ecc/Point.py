import numbers

from src.ecc.FieldInt import FieldInt


class Point(object):
    def __init__(self, x: FieldInt, y: FieldInt, z: FieldInt, a: FieldInt, b: FieldInt, mod: object):
        """
        :param x: The X coordinate in the projective space
        :param y: The Y coordinate in the projective space
        :param z: The Z coordinate in the projective stace
        :param a: The a coefficient of the elliptic curve
        :param b: The b coefficient of the elliptic curve
        :param mod: The modulus
        """

        # Sanity checks
        if x is not None and not isinstance(x, FieldInt):
            # x coordinate: FieldInt|None
            raise ValueError("Expecting a FieldInt or None for x coordinate, got {}".format(x))
        if y is not None and not isinstance(y, FieldInt):
            # y coordinate: FieldInt|None
            raise ValueError("Expecting a FieldInt or None for x coordinate, got {}".format(y))
        if z is not None and not isinstance(z, FieldInt):
            # z coordinate: FieldInt|None
            raise ValueError("Expecting a FieldInt or None for x coordinate, got {}".format(z))
        if not isinstance(a, FieldInt):
            # a EC parameter: FieldInt
            raise ValueError("Expecting a FieldInt for a parameter, got {}".format(a))
        if not isinstance(b, FieldInt):
            # b EC parameter: FieldInt
            raise ValueError("Expecting a FieldInt for b parameter, got {}".format(a))
        if x is not None \
                and (x.modulus != mod or y.modulus != mod or z.modulus != mod) \
                or a.modulus != mod or b.modulus != mod:
            raise ValueError("Moduli must match")

        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.modulus = mod

    def factory(self, x, y, z):
        """
        Generate a new Point based on the current curve and modulus.
        :param x: The new X coordinate
        :param y: The new Y coordinate
        :param z: The new Z coordinate
        :return:
        """
        return Point(x, y, z, self.a, self.b, self.modulus)

    def is_zero(self):
        """
        Check if the point is zero (i.e. is X coordinate is not defined).
        :return:
        """
        return self.x is None

    def is_on_curve(self) -> bool:
        """
        Check if the point is on the curve E(a,b), regarding its x,y,z coordinates.
        The quality to check is: y^2*z = x^3 + a*x*z^2 + b*z^2
        :return:
        """
        return not self.is_zero() and \
               self.y * self.y * self.z == \
               self.x * self.x * self.x + self.a * self.x * self.z * self.z + self.b * self.z * self.z * self.z

    def __add__(self, other):
        """
        Add two Point objects.
        :param other: The other Point.
        :return:
        """
        # Sanity checks
        if not isinstance(other, Point):
            # Instance compatibility
            raise TypeError("Expected ProjectiveCurvePoint")
        if (self.a, self.b, self.modulus) != (other.a, other.b, other.modulus):
            # Modulus compatibility
            raise ValueError("Other point must have same parameters")

        # Do not compute anything if one of the members is zero
        if self.is_zero():
            return other
        elif other.is_zero():
            return self

        # Prepare the projective variables
        t0 = self.y * other.z
        t1 = other.y * self.z
        u0 = self.x * other.z
        u1 = other.x * self.z

        if u0 == u1:
            if t0 == t1:
                # x1*z2 = x2*z1 and y1*z2=y2*z1 -> the Points are the same, simply double
                return self.double()
            else:
                return self.factory(None, None, None)
        else:
            # Finish the computation of the projective variables
            t = t0 - t1
            u = u0 - u1
            u2 = u * u
            v = self.z * other.z
            w = t * t * v - u2 * (u0 + u1)
            u3 = u * u2
            rx = u * w
            ry = t * (u0 * u2 - w) - t0 * u3
            rz = u3 * v
            return self.factory(rx, ry, rz)

    def double(self):
        """
        Optimized function to double a Point (will be used in the fast scalar multiplication).
        :return:
        """
        if self.is_zero() or self.y == 0:
            return self.factory(None, None, None)
        else:
            two = FieldInt(2, self.modulus)
            t = self.x * self.x * FieldInt(3, self.modulus) + self.a * self.z * self.z
            u = self.y * self.z * two
            v = u * self.x * self.y * two
            w = t * t - v * two
            rx = u * w
            ry = t * (v - w) - u * u * self.y * self.y * two
            rz = u * u * u
            return self.factory(rx, ry, rz)

    def __neg__(self):
        """
        Implementation of the negative operator.
        :return:
        """
        if self.is_zero():
            return self
        else:
            return self.factory(self.x, -self.y, self.z)

    def __sub__(self, other):
        """
        Implementation of the substraction (via negative an additive operators).
        :param other:
        :return:
        """
        return self + -other

    def __mul__(self, n):
        """
        Implementation of the scalar multiplication.
        :param n: The scalar (must be an integer).
        :return:
        """
        if not isinstance(n, numbers.Integral):
            raise TypeError("Expected integer")
        if n < 0:
            return -self * -n

        result = self.factory(None, None, None)
        temp = self

        # Optimized multiplication
        while n != 0:
            if n & 1 != 0:
                result += temp

            temp = temp.double()  # Double if n is even (much faster!)
            n >>= 1

        return result

    def __eq__(self, other):
        """
        Implementation of the equality operator, in the projective coordinates.
        :param other:
        :return:
        """
        if self.is_zero() or other.is_zero():
            return self.is_zero() and other.is_zero()
        else:
            return isinstance(other, Point) and \
                   (self.x * other.z, self.y * other.z, self.a, self.b, self.modulus) == \
                   (other.x * self.z, other.y * self.z, other.a, other.b, other.modulus)

    def __ne__(self, other):
        """
        Implementation of the not equals operator.
        :param other:
        :return:
        """
        return not (self == other)

    def __str__(self):
        if self.is_zero():
            return "(Zero)"
        else:
            return "({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "Point (projective coordinates) (x={}, y={}, z={}, a={}, b={}, mod={})" \
            .format(self.x, self.y, self.z, self.a, self.b, self.modulus)
