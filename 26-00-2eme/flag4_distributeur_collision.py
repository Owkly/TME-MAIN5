import hashlib
import numpy as np
from ast import literal_eval


def f(x):
    return (hashlib.sha256(name+(x)).digest()[:7])


def brent(f, x0):
    power = lam = 1
    tortoise = x0
    hare = f(x0)
    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1

    tortoise = hare = x0
    for i in range(lam):
        hare = f(hare)

    mu = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1

    return lam, mu


name = b"Ryann"
x = b'5'
l, m = brent(f, x)
for i in range(m-1):
    x = f(x)
x1 = x
for i in range(l):
    x = f(x)
x2 = x

# Affichage des résultats
print("Vérification des hachages:")
print(hashlib.sha256(name + x1).hexdigest())
print(hashlib.sha256(name + x2).hexdigest())

print("\nLes deux clef sont:")
print((name + x1).hex())
print((name + x2).hex())
