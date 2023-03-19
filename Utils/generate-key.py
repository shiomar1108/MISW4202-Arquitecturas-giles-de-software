from cryptography.fernet import Fernet

def genwrite_key():
    key = Fernet.generate_key()
    with open("security.key", "wb") as key_file:
        key_file.write(key)
        
genwrite_key()