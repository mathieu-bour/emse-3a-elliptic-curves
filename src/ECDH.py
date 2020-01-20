from random import randint
from src.lib.P256 import P256

# Standard generator
G = P256.Generator()

# Alice chooses a key ka
ka = randint(1, P256.m)
print("Alice's key: {}".format(ka))
# Bob chooses a key kb
kb = randint(1, P256.m)
print("Bob's key: {}".format(kb))

PA = G * ka
print("Alice sends: {}".format(PA))
PB = G * kb
print("Bob sends: {}".format(PB))

PAB = PA * kb
print("Alice got: {}".format(PAB))
PBA = PB * ka
print("Bob got: {}".format(PBA))

print("Comparaison: {}".format(PAB == PBA))
