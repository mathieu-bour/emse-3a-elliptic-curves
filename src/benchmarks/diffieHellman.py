from time import time_ns
from src.ecc.P256 import P256
from random import randint

nstime = lambda: int(round(time_ns()))
interations = 10 ** 4

G = P256.Generator()

def diffie_hellman():
    ka = randint(1, P256.m)
    print("Alice's key: {}".format(ka))
    kb = randint(1, P256.m)
    print("Bob's key: {}".format(kb))
    PA = G * ka
    # print("Alice sends: {}".format(PA))
    PB = G * kb
    # print("Bob sends: {}".format(PB))

    PAB = PA * kb
    # print("Alice got: {}".format(PAB))
    PBA = PB * ka
    # print("Bob got: {}".format(PBA))
    assert (PAB == PBA)
    # print("Comparaison: {}".format(PAB == PBA))

start = nstime()
for i in range(interations):
    diffie_hellman()

diff = nstime() - start
per_seconds = round(interations / (diff / 10 ** 9), 3)
print("Diffie Helman exchanges per sec : {}/s".format(per_seconds))