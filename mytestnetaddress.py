from ecc import PrivateKey
from helper import hash256, little_endian_to_int

mypass = b'KBU_201601071_PARKDONGHYUNE'
mysecret = little_endian_to_int(hash256(mypass))


P = PrivateKey(mysecret)

print(P.point.address(testnet=True))
