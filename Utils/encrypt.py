from cryptography.fernet import Fernet

# Function to load the key
def load_security_key(key):
    return open(key, "rb").read()

# location key
locationkey = input('Ingrese la ruta del key\n')
key = load_security_key(locationkey)
# location key
stringToEncrypt = input('Ingrese el text a encriptar\n')
encrypt = Fernet(key)
encryptedValue = encrypt.encrypt(stringToEncrypt.encode())
print(encryptedValue)