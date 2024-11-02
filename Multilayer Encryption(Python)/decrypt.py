import json
import base64
from key_gen import gen_key
import hashlib


# Importing decryption algorithms
from bin.aes128 import decrypt as aes128_decrypt
from bin.aes256 import decrypt as aes256_decrypt
from bin.aesgcm import decrypt as aesgcm_decrypt
from bin.blowfish import decrypt as blowfish_decrypt
from bin.arc4 import decrypt as arc4_decrypt
from bin.chacha20poly1305 import decrypt as chacha20poly1305_decrypt
from bin.des3 import decrypt as des3_decrypt
from bin.rc4 import decrypt as rc4_decrypt
from bin.salsa20 import decrypt as salsa20_decrypt
from bin.xchacha20 import decrypt as xchacha20_decrypt
# from bin.shacal import decrypt as shacal_decrypt

# Function to read the encrypted PDF file and convert it to bytes
def read_encrypted_pdf(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Function to save the decrypted PDF data
def save_decrypted_data(decrypted_data, output_path):
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)

# Function to read the hash from the hash file
def read_hash_file(hash_file_path):
    with open(hash_file_path, 'r') as file:
        return file.read().strip()

# Function to create the SHA-256 hash of PDF content
def create_sha256_hash(pdf_content):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(pdf_content)
    return sha256_hash.hexdigest()

# Function to check if the hash matches the PDF file's hash
def verify_pdf_hash(pdf_content, hash_file_path):
    # Read the PDF content and the stored hash
    # pdf_content = read_pdf(pdf_file_path)
    stored_hash = read_hash_file(hash_file_path)
    
    # Generate the SHA-256 hash for the PDF content
    pdf_hash = create_sha256_hash(pdf_content)
    
    # Compare and print the result
    if pdf_hash == stored_hash:
        print("The hash matches the PDF file's hash.")
        return True
    else:
        print("The hash does not match the PDF file's hash.")
        return False

# Function to decrypt PDF using specified algorithms
def decrypt_pdf(encrypted_pdf_path, layers, algorithms, all_passphrases, all_salts, output_file_path):
    # Read the encrypted PDF data
    pdf_data = read_encrypted_pdf(encrypted_pdf_path)

    # Load nonces from the corresponding file
    nonce_file_path = encrypted_pdf_path + '.nonces.json'
    with open(nonce_file_path, 'r') as nonce_file:
        nonces = json.load(nonce_file)

    # Decrypt in reverse order
    for algo, nonce_b64,passphrase,salt in zip(reversed(algorithms), reversed(nonces), reversed(all_passphrases), reversed(all_salts)):
        nonce = base64.b64decode(nonce_b64.encode('utf-8'))  # Decode from base64
        # print(f"algo:{algo}")
        # print(f"nonce_b64:{nonce_b64}")
        # print(f"passphrase:{passphrase}")
        # print(f"salt:{salt}")
        print(f"Decrypting using: {algo} with nonce: {nonce_b64}")  # Debug statement
        key=""
        if algo == 'aes128':
            key=gen_key(algo,passphrase,salt)
            pdf_data = aes128_decrypt(pdf_data, key, nonce)
        elif algo == 'aes256':
            key=gen_key(algo,passphrase,salt)
            pdf_data = aes256_decrypt(pdf_data, key, nonce)
        elif algo == 'aesgcm':
            key=gen_key(algo,passphrase,salt)
            pdf_data = aesgcm_decrypt(pdf_data, key, nonce) 
        elif algo == 'blowfish':
            key=gen_key(algo,passphrase,salt)
            pdf_data = blowfish_decrypt(pdf_data, key, nonce)
        elif algo == 'arc4':
            key=gen_key(algo,passphrase,salt)
            pdf_data = arc4_decrypt(pdf_data, key, nonce)
        elif algo == 'chacha20poly1305':
            key=gen_key(algo,passphrase,salt)
            pdf_data = chacha20poly1305_decrypt(pdf_data, key, nonce)
        elif algo == 'des3':
            key=gen_key(algo,passphrase,salt)
            pdf_data = des3_decrypt(pdf_data, key, nonce)
        elif algo == 'rc4':
            key=gen_key(algo,passphrase,salt)
            pdf_data = rc4_decrypt(pdf_data, key, nonce)
        elif algo == 'salsa20':
            key=gen_key(algo,passphrase,salt)
            pdf_data = salsa20_decrypt(pdf_data, key, nonce)
        elif algo == 'xchacha20':
            key=gen_key(algo,passphrase,salt)
            pdf_data = xchacha20_decrypt(pdf_data, key, nonce)
        # elif algo == 'shacal':
        #     key=gen_key(algo,passphrase,salt)
        #     pdf_data = shacal_decrypt(pdf_data, key, nonce)
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

    hash_location=f"{encrypted_pdf_path}.hash"
    print(f"hash_location:{hash_location}")
    if(verify_pdf_hash(pdf_data, hash_location)):
        save_decrypted_data(pdf_data, output_file_path)
        print(f"File decrypted and saved to {output_file_path}")
    else:
        print("incorrect Passphrases, Try Again")

def get_valid_passphrase(layer):
    while True:
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



# Main function to get user input and start decryption
if __name__ == "__main__":
    encrypted_pdf = input("Enter the encrypted PDF file path: ")
    output_file_path = input("Enter the output decrypted file path: ")
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


    # Call the decryption function
    decrypt_pdf(encrypted_pdf,layers, selected_algos, all_passphrases,all_salts, output_file_path)
