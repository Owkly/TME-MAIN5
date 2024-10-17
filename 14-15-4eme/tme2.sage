# Importer toutes les fonctions nécessaires de SageMath
from sage.all import *

# Paramètres donnés
p = int('e935748016029a1b103673c41aac14b55cdb3dae59515ffe94c0476ba2526f4b77c610e88d07bb832df5998937430c5076c02f030fa4acf267dd40b39fd06fe8b38963500c57c387a1d33672e87d59ba598fb3bcd86af08ad266d324893c960bd052394bf0ae98d25ad5a927a78540e2a55bc284973d5328a48d3f8ce54aa03b', 16)
x = int('2f1eb0b21f02bf25cca9261d1ae5303595b79a4fb4608055385272862972d004a4f7738762907a0937fe0a21227875d562228de4a5869905bea7b42af66c969c1dd7c44a415622cee64974c5e2aed0c7f8c3a0310b26b1af0c7f1b3d9750176bc9566751ad801c2c01f9169b1923814997780be3209d12d9c15f110351f6d118', 16)

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
    print(f"a en base 10 : {a_base10}")
    print(f"b en base 10 : {b_base10}")
else:
    print("Les valeurs trouvées ne respectent pas les contraintes de taille.")
