# Smart Locker

## PDF Encryption and Decryption Flask API

This project provides a Flask-based API for encrypting and decrypting PDF files. It supports multiple encryption algorithms, customizable watermarking, and file integrity verification using SHA-256 hashes. The API handles file uploads and offers flexibility for secure PDF processing.

### Features

#### Encryption

- Supports multiple encryption algorithms:
- AES128, AES256, AES-GCM, Blowfish, ARC4, ChaCha20-Poly1305, DES3, RC4, Salsa20, XChaCha20.
- Dynamically generates encryption keys and nonces.
- Outputs encrypted files, associated metadata, and integrity hash in a downloadable ZIP archive.

#### Decryption

- Accepts individual files or a ZIP archive containing encrypted data, nonces, and hash.
- Validates file integrity using SHA-256 hash.
- Returns the decrypted file with an optional watermark.

#### Watermarking
- Customizable options:
  - Text, color, font, size, angle, and opacity.
- Ensures visually secure output.

#### Error Handling
- Returns descriptive error messages for invalid input, tampered files, or incorrect parameters.
- Supports validation for JSON input, file formats, and encryption parameters.

### Requirements

#### Dependencies

- Install the following Python packages:
  ```bash
  pip install -r requirements.txt
  ```

#### Folder Structure
- Ensure the bin folder contains:
  - keygen.py (for generating encryption keys).
  - Encryption and decryption algorithm implementations..

### API Endpoints

#### `/encrypt` (POST)

Encrypts a provided PDF file using the selected algorithms.

- **Request**
  - Files:
    - original_pdf: The PDF file to be encrypted.

- **Form Data:**
  - `data` (JSON string): Encryption parameters:
    ```json
    {
      "selected_algos": ["aes256", "blowfish"],
      "all_passphrases": ["pass1", "pass2"],
      "filename": "sample"
    }
    ```

**Response**

A ZIP archive containing:
- encrypted.enc: Encrypted PDF data.
- encrypted.nonces.json: Nonces used for encryption.
- encrypted.hash: SHA-256 hash of the original PDF.

**Example**
```bash
curl -X POST -F "original_pdf=@path/to/file.pdf" \
     -F 'data={"selected_algos": ["aes256"], "all_passphrases": ["mypassword"], "filename": "test"}' \
     http://localhost:5000/encrypt -o encrypted_files.zip
```


#### `/decrypt` (POST)

Decrypts an encrypted PDF file.

- **Request**
  - Files:
    - encrypted_files.zip: ZIP archive containing encrypted data, nonces, and hash.

  - Or individual files:
    - encrypted.enc: Encrypted PDF data.
    - encrypted.nonces.json: Nonces used for decryption.
    - encrypted.hash: SHA-256 hash.

- **Form Data:**

  - `data` (JSON string): Decryption parameters:
```json
{
  "selected_algos": ["aes256"],
  "all_passphrases": ["mypassword"],
  "filename": "test",
  "watermark_text": "Confidential",
  "watermark_color": "#FF0000",
  "watermark_size": 50,
  "watermark_angle": 45,
  "watermark_opacity": 50,
  "watermark_font": "Helvetica"
}
```

- **Response**
  - A watermarked, decrypted PDF file.

- **Example**
```bash
curl -X POST -F "encrypted_files.zip=@path/to/encrypted_files.zip" \
     -F 'data={"selected_algos": ["aes256"], "all_passphrases": ["mypassword"], "filename": "test", "watermark_text": "Confidential"}' \
     http://localhost:5000/decrypt -o decrypted_file.pdf
```

### Customization

#### Encryption Algorithms

To add or modify encryption algorithms, follow these steps:

1. File Naming: Create a Python file in the bin folder with the naming convention algorithm_name.py (e.g., aes128.py).

2. Implementation: Define the encryption and decryption functions in the new file. These functions should follow this structure:

  - `encrypt(data, key, nonce_length)`: Accepts data to encrypt, the encryption key, and the nonce length. Returns the encrypted data and nonce.

  - `decrypt(data, key, nonce)`: Accepts encrypted data, the encryption key, and the nonce. Returns the decrypted data.

    **Example:**
    ```python
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes

    def encrypt(data, key, nonce_length):
        nonce = get_random_bytes(nonce_length)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        ciphertext = cipher.encrypt(data)
        return ciphertext, nonce

    def decrypt(data, key, nonce):
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        return cipher.decrypt(data)
    ```
3. Update Imports: Add the new algorithm to the __init__.py file in the bin folder:

    ```python
    from .algorithm_name import encrypt as algorithm_name_encrypt, decrypt as algorithm_name_decrypt
    ```
4. Testing: Test the new algorithm to ensure it integrates seamlessly with the API.
- Verify encryption and decryption produce consistent results.
- Check compatibility with existing endpoints.

#### Watermarking

To customize or enhance watermarking functionality, you can update the logic in the add_watermark_to_pdf function. Watermarking involves overlaying visible text or graphics on a PDF, typically for branding, identification, or security purposes. Here’s how you can modify and extend this feature in detail:

1. Parameters: Update the function to accept additional parameters, such as:
  - text: The watermark text to overlay.
  - font: The font style (e.g., Helvetica, Times New Roman).
  - size: Font size for the watermark.
  - color: RGB or HEX code for the watermark color.
  - angle: The rotation angle of the watermark (e.g., diagonal placement).
  - opacity: Transparency level of the watermark (0-100%).

2. Implementation: Use a PDF manipulation library like PyPDF2 or ReportLab to draw the watermark on each page of the PDF.

    Example implementation:
    ```python
    from reportlab.pdfgen import canvas
    from PyPDF2 import PdfReader, PdfWriter
    from io import BytesIO

    def add_watermark_to_pdf(input_pdf_path, output_pdf_path, text, font, size, color, angle, opacity):
        # Create a PDF with the watermark
        watermark_buffer = BytesIO()
        c = canvas.Canvas(watermark_buffer)
        c.setFont(font, size)
        c.setFillColorRGB(*color)  # Assuming color is an RGB tuple
        c.translate(300, 500)  # Position the watermark
        c.rotate(angle)
        c.drawString(0, 0, text)
        c.save()

        watermark_buffer.seek(0)
        watermark_pdf = PdfReader(watermark_buffer)
        input_pdf = PdfReader(input_pdf_path)
        output_pdf = PdfWriter()

        # Merge watermark with each page
        for page in input_pdf.pages:
            page.merge_page(watermark_pdf.pages[0])
            output_pdf.add_page(page)

        with open(output_pdf_path, 'wb') as output_file:
            output_pdf.write(output_file)
    ```

3. Testing:
- Ensure the watermark appears correctly on all pages of the PDF.
- Test various fonts, sizes, colors, and angles to verify flexibility.
- Validate that the watermark does not obscure critical content in the document.

4. Advanced Customizations:
- Add support for image-based watermarks (e.g., company logos).
- Implement conditional watermarking, where different pages have unique watermarks.
- Include metadata or invisible watermarks for digital tracking.

By enhancing the add_watermark_to_pdf function, you can tailor the watermarking feature to meet specific requirements for your project. watermarking logic in the add_watermark_to_pdf function for advanced customization.
