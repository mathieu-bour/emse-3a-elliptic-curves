from time import time_ns

from src.ecc.P256 import P256

nstime = lambda: int(round(time_ns()))
interations = 10 ** 3

keys = [0] * interations

for i in range(interations):
    keys[i] = P256.random()

start = nstime()

for i in range(interations):
    G = P256.Generator()
    C = G * keys[i]

diff = nstime() - start
per_seconds = round(interations / (diff / 10 ** 9), 3)

print("Signatures : {}/s".format(per_seconds))
