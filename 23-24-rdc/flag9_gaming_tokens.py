import hashlib
from Crypto.Cipher import AES
import binascii

# Générer une graine
seed = bytes.fromhex('ffeeddccbbaa99887766554433221100')

# Fonction pour générer les noeuds de l'arbre de PRNGs avec des clés de 128 bits
def generate_prng_tree(seed, depth=10):
    A = {1: seed}
    for i in range(1, 2 ** depth):
        sha256 = hashlib.sha256(A[i]).digest()
        A[2 * i] = sha256[:16]  # 128 bits pour chaque branche de l'arbre
        A[2 * i + 1] = sha256[16:32]
    return A

# Fonction pour chiffrer avec AES-128
def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)

# Générer les paires K[i], X[i], Y[i]
def generate_tokens(A, n=1024):
    K = {}
    pairs = {}
    for i in range(n):
        K[i] = A[i + 1024]  # Utiliser les clés de 128 bits
        X_i = aes_encrypt(K[i], b'\x00' * 16)
        Y_i = aes_encrypt(K[i], b'\xff' * 16)
        # Combiner X[i] et Y[i] en un seul bloc de 256 bits
        pairs[i] = X_i + Y_i
    return K, pairs

# Calcul du commitment
def calculate_commitment(pairs):
    concatenated = b''.join(pairs[i] for i in range(len(pairs)))
    return hashlib.sha256(concatenated).hexdigest()

# Fonction pour calculer le co-chemin
def calculate_co_path(A, i, depth=10):
    co_path = []
    j = i + 1024  # L'indice dans l'arbre est i + 1024
    for _ in range(depth):
        # Ajouter le frère (j XOR 1) au co-chemin
        co_path.append(A[j ^ 1])
        j //= 2
    return co_path

# Fonction pour révéler le pair et le co-chemin
def reveal_pair_and_co_path(i, pairs, A):
    # Révéler la paire X[i] || Y[i]
    print(f"\nPair X[{i}] || Y[{i}] :", binascii.hexlify(pairs[i]).decode())
    
    # Calculer et révéler le co-chemin
    co_path = calculate_co_path(A, i)
    print("\nCo-path in PRNG tree (10 * 128 bits, hex, 1 per line):")
    for idx, node in enumerate(co_path):
        print(binascii.hexlify(node).decode())

# Exemple d'utilisation
def main():
    # Demander à l'utilisateur l'indice i
    while True:
        try:
            i = int(input("Veuillez entrer l'indice i (0 <= i < 1024) : "))
            if 0 <= i < 1024:
                break
            else:
                print("L'indice doit être compris entre 0 et 1023.")
        except ValueError:
            print("Veuillez entrer un entier valide.")

    # Révéler le pair et le co-chemin pour l'indice choisi
    reveal_pair_and_co_path(i, pairs, A)

# Génération des données
A = generate_prng_tree(seed)  # Arbre PRNG
K, pairs = generate_tokens(A)  # Génération des paires

# Calcul et affichage du commitment
commitment = calculate_commitment(pairs)
print("Commitment:", commitment)

# Exécution principale
main()


# pour i = 340
# Signature: 3036021900F6F58B85359F8DCC8938C92B554DA903906F47544C11CB55021900ED7F74646240F8E7BF6DB61BCA6DF8DE9FDDD08F8DA4C5EE