from cryptography.fernet import Fernet
import os

KEY_FILE_PATH = "authentication.key"


# Generate a key for encryption and decryption
def generate_key():
    return Fernet.generate_key()

# Save the key to a file
def save_key_to_file(key, file_path):
    with open(file_path, "wb") as key_file:
        key_file.write(key)

# Load the key from a file
def load_key_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as key_file:
            return key_file.read()
    else:
        # If the file doesn't exist, generate a new key
        key = generate_key()
        save_key_to_file(key, file_path)
        return key
    
key = load_key_from_file(KEY_FILE_PATH)


# Encrypt two strings into one key
def obtain_token(string1, string2):
    cipher_suite = Fernet(key)
    encrypted_string1 = cipher_suite.encrypt(string1.encode())
    encrypted_string2 = cipher_suite.encrypt(string2.encode())
    combined_encrypted_key = encrypted_string1 + encrypted_string2
    return combined_encrypted_key

def obtain_credentials(combined_encrypted_key):
    cipher_suite = Fernet(key)
    size = len(combined_encrypted_key) // 2
    encrypted_string1 = combined_encrypted_key[:size]
    encrypted_string2 = combined_encrypted_key[size:]
    decrypted_string1 = cipher_suite.decrypt(encrypted_string1).decode()
    decrypted_string2 = cipher_suite.decrypt(encrypted_string2).decode()
    return decrypted_string1, decrypted_string2

