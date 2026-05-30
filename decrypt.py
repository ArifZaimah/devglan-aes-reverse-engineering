from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Devglan's hardcoded fixed 16-byte initialization vector
DEVGLAN_IV = b"565659iu8ghbv567"

while True:
    print("\n" + "="*45)
    print("=== DEVGLAN-COMPATIBLE LOCAL TOOL ===")
    print("1. Encrypt text (Output can be decrypted on Devglan)")
    print("2. Decrypt text (Input from Devglan form)")
    print("3. Exit Program")
    print("="*45)
    
    choice = input("Select an option (1, 2, or 3): ").strip()
    
    if choice == '3':
        print("\nExiting program. Goodbye!")
        break
        
    if choice in ['1', '2']:
        user_text = input("Enter Text / Cipher string: ").strip()
        user_key = input("Enter Secret Key (Must be 16 chars): ").strip()

        if len(user_key) != 16:
            print(f"\n[Error] Key must be exactly 16 characters long! (Current length: {len(user_key)})")
            continue
            
        key_bytes = user_key.encode('utf-8')
        
        if choice == '1':
            # Replicate Devglan Encryption exactly
            cipher = AES.new(key_bytes, AES.MODE_CBC, DEVGLAN_IV)
            padded_data = pad(user_text.encode('utf-8'), AES.block_size)
            encrypted_bytes = cipher.encrypt(padded_data)
            ciphertext_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            print(f"\n[SUCCESS] Encrypted String: {ciphertext_b64}")
            
        elif choice == '2':
            # Replicate Devglan Decryption exactly
            try:
                # Automatically fix missing Base64 structural padding if omitted
                if len(user_text) % 4 != 0:
                    user_text += "=" * (4 - (len(user_text) % 4))
                    
                raw_ciphertext = base64.b64decode(user_text)
                cipher = AES.new(key_bytes, AES.MODE_CBC, DEVGLAN_IV)
                decrypted_bytes = cipher.decrypt(raw_ciphertext)
                plaintext = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
                print(f"\n[SUCCESS] Decrypted Text Result: {plaintext}")
            except Exception as e:
                print(f"\n[Error] Decryption failed! Ensure key and text match: {e}")
    else:
        print("\n[Error] Invalid choice. Please select 1, 2, or 3.")
