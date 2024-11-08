from sympy import mod_inverse
from Crypto.PublicKey import DSA
from Crypto.Random import random
from Crypto.Util.number import bytes_to_long
from asn1crypto.core import Sequence, Integer
import hashlib

# Extraction de la clé publique pour récupérer les paramètres p, q, g
f = open("MOHAB_pk.pem", "r")
key = DSA.import_key(f.read())
p = key.p
q = key.q
g = key.g
f.close()

# Signatures des anciens emails (correctes)
signature1 = "3046022100CCAD8AF15EAC3FBC134442440776F60774CBED4C2B8E13E3EC838CA6D667DA2A022100ED9E124FBEFBC3A9E9B6AE0EB0BD676CA5513AA9D1939C3AE1C2234FA34E16B9"
signature2 = "3046022100BCAB8AC845751C356E9005CA1D2EF6257C08CCDBE7AD88E3A8320090C924FCBC022100E65A30B0E4C18C429E9FF326C78EFE007EE6101D1D9857579D9D7FAE79343514"

# Message à signer pour le nouveau challenge
message = "sprat eater julep welch vower"

# Fonction pour extraire c et s à partir des signatures
def extract_signature_parts(signature):
    c = signature[10:74]  # c commence après le préfixe DER (3046...0221)
    s = signature[76:]    # s commence après la deuxième 0221
    return int(c, 16), int(s, 16)

c1, s1 = extract_signature_parts(signature1)
c2, s2 = extract_signature_parts(signature2)

# Calcul de la différence des signatures et des défis
delta_s = (s1 - s2) % q
delta_c = (c1 - c2) % q

# Calcul de l'inverse modulaire de delta_c
inv_delta_c = mod_inverse(delta_c, q)

# Calcul de la clé secrète x
x = (delta_s * inv_delta_c) % q
print(f"Clé secrète x: {hex(x)}")

# Étape 1: Choisir un nonce k aléatoire
k = random.randint(1, q-1)

# Étape 2: Calculer r = g^k mod p
r = pow(g, k, p)

# Étape 3: Calculer c = SHA256(M || r), où r est encodé sur 2048 bits
r_bytes = r.to_bytes(256, byteorder='big')  # Encodage de r sur 2048 bits (256 octets)
message_bytes = message.encode('utf-8')
hash_input = message_bytes + r_bytes
c = bytes_to_long(hashlib.sha256(hash_input).digest()) % q

# Étape 4: Calculer s = k + c * x mod q (en utilisant la clé privée calculée x)
s = (k + c * x) % q

# Étape 5: Encodage ASN.1 en DER pour créer la signature
class Signature(Sequence):
    _fields = [
        ('c', Integer),
        ('s', Integer)
    ]

# Créer la séquence contenant c et s
signature = Signature({
    'c': Integer(c),
    's': Integer(s)
})

# Obtenir la signature encodée en DER
signature_der = signature.dump()

# Afficher la signature finale en hexadécimal
print(f"Signature DER: {signature_der.hex()}")
