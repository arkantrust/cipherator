from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import secrets
import base64
import os

# Generate a 32-byte key for AES encryption
def gen_key():
    key_bytes = secrets.token_bytes(32)
    key_base64 = base64.b64encode(key_bytes).decode('utf-8')
    return key_base64

def pad(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def unpad(data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def cipher_file(filename, key):
    cipher = Cipher(algorithms.AES(key), modes.CFB8(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(filename, 'rb') as file:
        file_data = file.read()
    
    padded_data = pad(file_data)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    iv = cipher.mode.iv  # Initialization Vector used for encryption
    with open(filename + '.enc', 'wb') as file:
        file.write(iv + encrypted_data)  # Prepend IV to encrypted data

def decipher_file(filename, key):
    with open(filename, 'rb') as file:
        iv = file.read(16)  # Read the IV from the start of the file
        encrypted_data = file.read()
    
    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpad(decrypted_padded_data)
    
    output_file = filename.replace('.enc', '.dec')
    with open(output_file, 'wb') as file:
        file.write(decrypted_data)

def main():
    action = input("Would you like to cipher or decipher a file? (Enter 'cipher' or 'decipher'): ").strip().lower()
    filename = input("Enter the filename: ").strip()
    
    if action not in ['cipher', 'decipher']:
        print("Invalid action. Please choose 'cipher' or 'decipher'.")
        return
    
    key = get_key()
    
    if action == 'cipher':
        cipher_file(filename, key)
        print(f"File '{filename}' has been ciphered and saved as '{filename}.enc'")
    elif action == 'decipher':
        decipher_file(filename, key)
        print(f"File '{filename}' has been deciphered and saved as '{filename}.dec'")

if __name__ == "__main__":
    main()
