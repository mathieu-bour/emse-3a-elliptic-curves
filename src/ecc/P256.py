from random import randint

from src.ecc.FieldInt import FieldInt
from src.ecc.Point import Point


class P256:
    """
    Implementation of the constants of the P256 curve
    Reference: http://safecurves.cr.yp.to/equation.html
    """
    a = 3
    b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    m = 2 ** 251 - 1

    # Generator coordinates: https://crypto.stackexchange.com/q/41405
    xG = 48439561293906451759052585252797914202762949526041747995844080717082404635286
    yG = 2258390684796862237411570494974242622288194167061563441992324890848025900319

    @staticmethod
    def random():
        return randint(1, P256.m)

    @staticmethod
    def Generator() -> Point:
        """
        Get the standard generator for the curve.
        :return:
        """
        return Point(
            P256.FieldInt(P256.xG),
            P256.FieldInt(P256.yG),
            P256.FieldInt(1),
            P256.FieldInt(P256.a),
            P256.FieldInt(P256.b),
            P256.m
        )

    @staticmethod
    def FieldInt(value: int):
        return FieldInt(value % P256.m, P256.m)

    @staticmethod
    def Projective(x, y, z):
        return Point(
            P256.FieldInt(x),
            P256.FieldInt(y),
            P256.FieldInt(z),
            P256.FieldInt(P256.a),
            P256.FieldInt(P256.b),
            P256.m
        )
