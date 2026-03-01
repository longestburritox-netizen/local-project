import os
from cryptography.fernet import Fernet

# --------------------------
# Key Functions
# --------------------------

def generate_key(key_file='secret.key'):
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
    print(f"Key saved to {key_file}")
    return key

def load_key(key_file='secret.key'):
    return open(key_file, 'rb').read()

# --------------------------
# Encrypt One File
# --------------------------

def encrypt_file(file_path, key):
    fernet = Fernet(key)

    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(file_path + ".enc", 'wb') as f:
        f.write(encrypted)

    os.remove(file_path)  # 🔥 remove original file
    print(f"Encrypted: {file_path}")

# --------------------------
# Encrypt All Files in Folder
# --------------------------

def encrypt_directory(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:

            # Skip key file and already encrypted files
            if file.endswith(".enc") or file == "secret.key":
                continue

            full_path = os.path.join(root, file)
            encrypt_file(full_path, key)

# --------------------------
# Decrypt Without Creating .dec File
# --------------------------

def decrypt_file(file_path, key):
    fernet = Fernet(key)

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted = fernet.decrypt(encrypted_data)

    original_file = file_path.replace(".enc", "")

    with open(original_file, 'wb') as f:
        f.write(decrypted)

    os.remove(file_path)  # remove encrypted file
    print(f"Decrypted: {original_file}")

# --------------------------
# Example Usage
# --------------------------

if __name__ == "__main__":
    key_file = "secret.key"
    folder_to_encrypt = "src"  # 🔥 change this

    # Load or generate key
    key = load_key(key_file)
    # key = generate_key(key_file)

    # Encrypt everything inside folder
    encrypt_directory(folder_to_encrypt, key)

    # To decrypt a file later:
    # decrypt_file("my_folder/example.txt.enc", key)
