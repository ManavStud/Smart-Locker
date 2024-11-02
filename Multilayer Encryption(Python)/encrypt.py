import json
import base64
from key_gen import gen_key
import hashlib


# Importing encryption algorithms
from bin.aes128 import encrypt as aes128_encrypt
from bin.aes256 import encrypt as aes256_encrypt
from bin.aesgcm import encrypt as aesgcm_encrypt
from bin.blowfish import encrypt as blowfish_encrypt
from bin.arc4 import encrypt as arc4_encrypt
from bin.chacha20poly1305 import encrypt as chacha20poly1305_encrypt
from bin.des3 import encrypt as des3_encrypt
from bin.rc4 import encrypt as rc4_encrypt
from bin.salsa20 import encrypt as salsa20_encrypt
from bin.xchacha20 import encrypt as xchacha20_encrypt
# from bin.shacal import encrypt as shacal_encrypt


# Function to read the PDF file and convert it to bytes
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Function to save the encrypted PDF data
def save_encrypted_data(encrypted_data, output_path):
    with open(output_path, 'wb') as file:
        file.write(encrypted_data)

# Function to save the nonces to a JSON file
def save_nonces(nonces, nonce_file_path):
    with open(nonce_file_path, 'w') as nonce_file:
        json.dump(nonces, nonce_file)


# Function to encrypt PDF using specified algorithms
def encrypt_pdf(input_pdf_path, layers, algorithms, all_passphrases, all_salts, output_pdf_path):
    pdf_data = read_pdf(input_pdf_path)
    nonces = []

    # Encrypt in the order specified
    for algo,passphrase,salt in zip(algorithms,all_passphrases,all_salts):
        # print(f"algo:{algo}")
        # print(f"passphrase:{passphrase}")
        # print(f"salt:{salt}")

        key=""
        if algo == 'aes128':
            nonce_length = 12  # 96 bits for AES-GCM
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = aes128_encrypt(pdf_data, key, nonce_length)
        elif algo == 'aes256':
            nonce_length = 12  # 96 bits for AES-GCM
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = aes256_encrypt(pdf_data, key, nonce_length)
        elif algo == 'aesgcm':
            nonce_length = 12  # 96 bits for AES-GCM
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = aesgcm_encrypt(pdf_data, key, nonce_length)
        elif algo == 'blowfish':
            nonce_length = 4  # Blowfish typically uses an 8-byte nonce
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = blowfish_encrypt(pdf_data, key, nonce_length)
        elif algo == 'arc4':
            nonce_length = 8  # ARC4 typically uses an 8-byte nonce
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = arc4_encrypt(pdf_data, key, nonce_length)
        elif algo == 'chacha20poly1305':
            nonce_length = 12  # 96 bits for ChaCha20-Poly1305
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = chacha20poly1305_encrypt(pdf_data, key, nonce_length)
        elif algo == 'des3':
            nonce_length = 4  # 3DES typically uses an 8-byte nonce
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = des3_encrypt(pdf_data, key, nonce_length)
        elif algo == 'rc4':
            nonce_length = 8  # RC4 typically uses an 8-byte nonce
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = rc4_encrypt(pdf_data, key, nonce_length)
        elif algo == 'salsa20':
            nonce_length = 8  # Salsa20 typically uses an 8-byte nonce
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = salsa20_encrypt(pdf_data, key, nonce_length)
        elif algo == 'xchacha20':
            nonce_length = 24  # XChaCha20 typically uses a 24-byte nonce
            key=gen_key(algo,passphrase,salt)
            pdf_data, nonce = xchacha20_encrypt(pdf_data, key, nonce_length)
        # elif algo == 'shacal':
        #     nonce_length = 12  # XChaCha20 typically uses a 24-byte nonce
        #     key=gen_key(algo,passphrase,salt)
        #     pdf_data, nonce = shacal_encrypt(pdf_data, key, nonce_length)
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

        # Save the nonce as a base64 string
        nonces.append(base64.b64encode(nonce).decode('utf-8'))

    # Save the encrypted PDF file and the nonces
    save_encrypted_data(pdf_data, output_pdf_path)
    save_nonces(nonces, output_pdf_path + '.nonces.json')
    create_sha256_hash(input_pdf_path,output_pdf_path)

    print(f"Encryption complete. Encrypted file saved to {output_pdf_path}")
    print(f"Nonces saved to {output_pdf_path}.nonces.json")

def get_valid_passphrase(layer):
    while True:
        # passphrase = input("Enter a passphrase: ").
        passphrase=input(f"Enter Passphrase for Layer {layer}:")
        if 8 <= len(passphrase) <= 20:
            return passphrase
        else:
            print("Passphrase must be between 8 and 20 characters. Please try again.")

def extract_salt(passphrase):
    salt = ""
    if len(passphrase) % 2 == 0:
        # Fetch even-indexed characters if length is even
        salt = passphrase[1::2]
    else:
        # Fetch odd-indexed characters if length is odd
        salt = passphrase[0::2]
    return salt

def create_sha256_hash(input_file_path,output_file_path):
    # Read PDF content
    pdf_content = read_pdf(input_file_path)
    
    # Generate SHA-256 hash
    sha256_hash = hashlib.sha256()
    sha256_hash.update(pdf_content)
    hash_value = sha256_hash.hexdigest()
    
    # Print the hash
    print("SHA-256 Hash:", hash_value)
    
    # Create the output file path
    hash_output_file_path = f"{output_file_path}.hash"
    
    # Save the hash to a file
    with open(hash_output_file_path, 'w') as hash_file:
        hash_file.write(hash_value)
    
    print(f"Hash saved to: {hash_output_file_path}")

# Main function to get user input and start encryption
if __name__ == "__main__":
    input_pdf = input("Enter the input PDF file path: ")
    # Ask for output file path
    output_pdf = input("Enter the output encrypted file path: ")
    layers=int(input("Enter the No of Algorithms you want to use: "))
    selected_algos=[]
    available_algo=["aes128","aes256","aesgcm","arc4","blowfish","chacha20poly1305","des3","rc4","salsa20","xchacha20"]
    all_passphrases=[]
    all_salts=[]
    print("Select Algos")
    print("1. aes128\n2. aes256\n3. aesgcm\n4. arc4\n5. blowfish\n6. chacha20poly1305\n7. des3\n8. rc4\n9. salsa20\n10. xchacha20")
    for i in range(layers):
        while True:
            algo = int(input(f"Select Algo for Layer {i+1}: "))
            if 1 <= algo <= 10:
                selected_algos.append(available_algo[algo - 1])
                print(f"Algo Selected: {available_algo[algo - 1]}")
                passphrase=get_valid_passphrase(i+1)
                all_passphrases.append(passphrase)
                salt=extract_salt(passphrase)
                all_salts.append(salt)
                break
            else:
                print("Out of bound. Please select a valid algorithm number.")
    print(f"Final Selection {selected_algos}")
    print(f"all_passphrases=f{all_passphrases}")
    print(f"all_salts=f{all_salts}")



    # Call the encrypt function
    encrypt_pdf(input_pdf, layers, selected_algos, all_passphrases, all_salts, output_pdf)
    # encrypt_pdf(input_pdf_path, layers, algorithms, all_passphrases, salt, output_pdf_path)

