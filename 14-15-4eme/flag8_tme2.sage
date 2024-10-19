from sage.all import *

# Paramètres donnés
p = int('e9b327c84377f641c2e07b8e4f7d88e4f0dd3b3fc04eb6f9abd98327eda52437ec61e7f4880ec3c732c7d0210adb0b3f61bf15c3a9984105f44d2624c029bf1d119f704ba953d9ffee63d9dea2ff18728d2951effacb451ae740807d9bda9abda1f385c5b2705a897f3f7a1d7532d2e1873039ba15068adf070746622ea84fcf', 16)
x = int('4efc922b814af36fb0bfc9ed3ef38b3f3e1c40686e279916c089d6793d8566b27c28758bc595de788f5c1f4c57be55c836717fe8cc7109d872e824303333646775593286e0e385266f2eb85aea26381de4c96da247b253f7c89f6ac5ffe2b9d6443a910bf3c95a436c14c484cb568f1180d79ae04bb8c1749a693cb85ee382c7', 16)


# Calcul de la racine carrée de p
sqrt_p = floor(sqrt(p))

# Construction de la matrice pour le réseau
M = Matrix(ZZ, [[p, 0], [x, 1]])

# Réduction LLL
M_lll = M.LLL()

# Le vecteur court sera la première ligne de la matrice réduite
a, b = M_lll[0]

# Conversion en base 10 pour affichage sans préfixe hexadécimal
a_base10 = int(a)
b_base10 = int(b)

# Vérifier si les contraintes sont respectées et afficher en base 10
if abs(a) <= sqrt_p and abs(b) <= sqrt_p:
    print(f"a en base 10 : \n{a_base10}")
    print(f"b en base 10 : \n{b_base10}")
else:
    print("Les valeurs trouvées ne respectent pas les contraintes de taille.")
