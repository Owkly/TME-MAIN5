from Crypto.PublicKey import DSA


f = open("MOHAB_pk.pem", "r")
key = DSA.import_key(f.read())
print(key.p)
print(key.q)
print(key.g)
f.close()