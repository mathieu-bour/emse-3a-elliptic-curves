from hashlib import sha256

from src.ecc.P256 import P256

e = sha256()
e.update(b"resto en ville?")
e = e.digest()

da = P256.FieldInt(P256.random())
print("Got digest {}".format(e))
z = P256.FieldInt(int.from_bytes(e, byteorder='big'))
print("z = {}".format(z))
k = P256.random()
print("Got k {}".format(k))
P = P256.Generator() * k
r = P.x
s = P256.FieldInt(k).reciprocal() * (z + r * da)

print("Signature: r = {}, s = {}".format(r, s))
