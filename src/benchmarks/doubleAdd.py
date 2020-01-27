from time import time_ns
from src.ecc.P256 import P256

nstime = lambda: int(round(time_ns()))
interations = 10 ** 5

start = nstime()
for i in range(interations):
    G = P256.Generator()
    a = G * 2
diff = nstime() - start

per_seconds = round(interations / (diff / 10 ** 9), 3)
print("Double per sec: {}/s".format(per_seconds))

start = nstime()
for i in range(interations):
    G = P256.Generator()
    a = G + G
diff = nstime() - start

per_seconds = round(interations / (diff / 10 ** 9), 3)
print("Add per sec: {}/s".format(per_seconds))
