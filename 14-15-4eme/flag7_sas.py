from Crypto.PublicKey import RSA
import hashlib

# charge la clé puis extrait N et e
def load_public_key(pem_file: str):
    with open(pem_file, 'r') as f:
        public_key = RSA.import_key(f.read())
    return public_key.n, public_key.e

# hash le message
def sha256(message: str) -> bytes:
    hash_value = hashlib.sha256(message.encode()).digest()
    return hash_value

# créer un bloc PKCS#1 v1.5
def pad_pkcs1_v1_5(hash_value: bytes, N_len: int) -> int:
    # HASH_ID (SHA-256 OID)
    hash_id = b"\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20"
    
    # Calculer l'espace restant pour le padding
    total_length = N_len
    padding_length = total_length - len(hash_value) - len(hash_id) - 3  # 3 = \x00\x01 + \x00
    
    # Portion fixe de 10 octets de \xFF
    longueur = 10
    FF = b"\xFF" * longueur
    
    # Bourrage complémentaire pour ajuster la longueur
    autre_bourrage = b"\xFF" * (padding_length - longueur)
    
    # Construction du padding PKCS#1 v1.5 : \x00\x01, remplissage \xFF, \x00
    padding = b"\x00\x01" + FF + b"\x00"
    
    # Assembler le bloc final avec le complément de bourrage
    padded_block = padding + hash_id + hash_value + autre_bourrage
    print(f"block PKCS#1 v1.5: \n{padded_block.hex()}\n")
    
    return int.from_bytes(padded_block, byteorder="big")


# Calculer la racine cubique entière avec la méthode de Newton
def cube_root(x: int) -> int:
    guess = x >> (x.bit_length() // 3)
    while True:
        next_guess = (2 * guess + x // (guess ** 2)) // 3
        if next_guess >= guess:
            return guess
        guess = next_guess

# Étape 5: Forger la signature valide
def sign(message: str, pem_file: str) -> str:

    N, e = load_public_key(pem_file)
    N_len = N.bit_length() // 8
    hash_value = sha256(message)

    print(f"Taille du module n en octets: {N_len}")
    print(f"Module N: {hex(N)}")
    print(f"Exposant e: {e}")
    print(f"message : {message}")
    print(f"hash du message: {hash_value.hex()}\n")
    
    # Créer le padding PKCS#1 v1.5
    padded_block = pad_pkcs1_v1_5(hash_value, N_len)
    
    # Calculer une racine cubique exacte (en supposant que e = 3)
    signature = cube_root(padded_block)
    
    # Convertir la signature en hexadécimal pour la retourner
    signature_hex = hex(signature)[2:]  # Supprimer le '0x'
    
    # Vérifier la longueur de la signature et ajouter des zéros si nécessaire
    if len(signature_hex) < 2 * N_len:  # Remplir jusqu'à la taille correcte
        signature_hex = signature_hex.zfill(2 * N_len)
    
    print(f"Signature forgée (hex avec padding): \n{signature_hex}")
    
    return signature_hex

# Exemple d'utilisation
message = "PPTI SERVER ACCESS ON 2024-10-19 12:39 UTC"
pem_file = "ppti_pkey.pem"

# Forger la signature
signature = sign(message, pem_file)

print(len(signature))
