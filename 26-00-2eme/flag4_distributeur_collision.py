import hashlib

nom = b"Ryann"
valeur_initiale = b'1234'

def fonction_hachage(valeur):
    return hashlib.sha256(nom + valeur).digest()[:7]

def algo_brent(fonction_hachage, valeur_initiale):
    puissance = longueur_cycle = 1
    valeur_lente = valeur_initiale
    valeur_rapide = fonction_hachage(valeur_initiale)
    while valeur_lente != valeur_rapide:
        if puissance == longueur_cycle:
            valeur_lente = valeur_rapide
            puissance *= 2
            longueur_cycle = 0
        valeur_rapide = fonction_hachage(valeur_rapide)
        longueur_cycle += 1

    valeur_lente = valeur_rapide = valeur_initiale
    for i in range(longueur_cycle):
        valeur_rapide = fonction_hachage(valeur_rapide)

    position_debut_cycle = 0
    while valeur_lente != valeur_rapide:
        valeur_lente = fonction_hachage(valeur_lente)
        valeur_rapide = fonction_hachage(valeur_rapide)
        position_debut_cycle += 1

    return longueur_cycle, position_debut_cycle

longueur_cycle, position_debut_cycle = algo_brent(fonction_hachage, valeur_initiale)

# Calcul du premier point de collision
for i in range(position_debut_cycle - 1):
    valeur_initiale = fonction_hachage(valeur_initiale)
point_de_collision_1 = valeur_initiale

# Calcul du second point de collision
for i in range(longueur_cycle):
    valeur_initiale = fonction_hachage(valeur_initiale)
point_de_collision_2 = valeur_initiale

# Affichage des résultats
print("Vérification des hachages:")
print(hashlib.sha256(nom + point_de_collision_1).hexdigest())
print(hashlib.sha256(nom + point_de_collision_2).hexdigest())

print("\nLes deux points de collision sont :")
print(f"Point de collision 1 : {(nom + point_de_collision_1).hex()}")
print(f"Point de collision 2 : {(nom + point_de_collision_2).hex()}")
