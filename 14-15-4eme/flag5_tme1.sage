from sage.all import *

# Paramètres donnés
n = 7
a = int('0x5e9b0992596d5614', 16)
p = int('0xd92233fa14e75639', 16)
L = 2**56.07

# Initialisation de la matrice A (n x n)
A = Matrix(ZZ, n, n)

# Remplissage de la matrice
A[0, 0] = 1
# A_ii = p pour i > 0
for i in range(1, n):
    A[i, i] = p
# A_0j = a^j mod p pour j > 0
for j in range(1, n):
    A[0, j] = power_mod(a, j, p)

# Réduction de la matrice avec LLL pour trouver un vecteur court
A_lll = A.LLL()

# Chercher un vecteur court dans la première ligne de la matrice réduite
short_vector = A_lll[0]

# Calcul de la norme du vecteur court
norme_vecteur = sqrt(sum(x^2 for x in short_vector))

# Affichage des résultats si la norme est inférieure à L
if norme_vecteur < L:
    # Conversion en hexadécimal sans guillemets
    short_vector_hex = ", ".join(hex(x) for x in short_vector)
    print(f"Vecteur court en hexadécimal : ({short_vector_hex})")
else:
    print("Aucun vecteur court trouvé avec une norme inférieure à L.")
