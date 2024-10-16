openssl ecparam -genkey -name prime192v3 -out sk.pem
openssl ec -in sk.pem -pubout -out pk.pem

openssl dgst -sha256 -sign sk.pem -hex -out login-signature.bin login-challenge.txt