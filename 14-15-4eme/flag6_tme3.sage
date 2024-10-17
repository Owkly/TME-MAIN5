from sage.all import *

# Paramètre donné
p = int('dee00970ade8edbb7d1f3df0f6e88520cfe0dcfb51375ce43614486e9ee24dd4349ba2b66f505895f82aa3229e79d6c5924f464449669748a3596f78861c935d13a6adb328d23ae24301433982ed4dd16a47390d63a05564518f11836c2823cfaa5a35f3c293900b1dae90eb1a528de0ff94e300208e35ae3c1e9561f785c205', 16)

# Calculer beta tel que beta^2 = -1 mod p
beta = Mod(-1, p).sqrt()

# Initialisation de la matrice pour le réseau
M = Matrix(ZZ, 2, 2)
M[0, 0] = p
M[1, 0] = beta
M[1, 1] = 1

# Réduction LLL pour trouver un vecteur court (a, b)
M_lll = M.LLL()
a, b = M_lll[0]

# Vérification de la solution
if a**2 + b**2 == p:
    print(f"a = {a}, b = {b}")
else:
    print("Aucune solution trouvée avec ces valeurs de a et b.")
