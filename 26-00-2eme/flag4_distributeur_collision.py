import hashlib

nom = b"Ryann"
x = b'1234'

def hash(x):
    return hashlib.sha256(nom + x).digest()[:7]


def algo_brent(hash, x):
    power = periode = 1
    slow = x
    fast = hash(x)
    while slow != fast:
        if power == periode:
            slow = fast
            power *= 2
            periode = 0
        fast = hash(fast)
        periode += 1

    slow = fast = x
    for i in range(periode):
        fast = hash(fast)

    decalage = 0
    while slow != fast:
        slow = hash(slow)
        fast = hash(fast)
        decalage += 1

    return periode, decalage

periode, decalage = algo_brent(hash, x)

# Calcul de la première clef
for i in range(decalage - 1):
    x = hash(x)
x1 = x

# Calcul de la deuxième clef
for i in range(periode):
    x = hash(x)
x2 = x

# Affichage des résultats
print("Vérification des hachages:")
print(hashlib.sha256(nom + x1).hexdigest())
print(hashlib.sha256(nom + x2).hexdigest())

print("\nLes deux clefs sont :")
print(f"Clef 1 : {(nom + x1).hex()}")
print(f"Clef 2 : {(nom + x2).hex()}")
