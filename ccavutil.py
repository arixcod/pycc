#!/usr/bin/env python

from Crypto.Cipher import AES
import hashlib
from binascii import hexlify, unhexlify

# Padding function to make the data length a multiple of 16 bytes
def pad(data):
    length = 16 - (len(data) % 16)
    data += chr(length) * length
    return data

# Encryption function using AES in CBC mode
def encrypt(plainText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText)
    
    # Create MD5 hash of the working key
    encDigest = hashlib.md5()
    encDigest.update(workingKey.encode('utf-8'))  # Convert workingKey to bytes
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
    
    # Encrypt and convert to hex
    encryptedText = hexlify(enc_cipher.encrypt(plainText.encode('utf-8'))).decode('utf-8')
    return encryptedText

# Decryption function using AES in CBC mode
def decrypt(cipherText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    
    # Create MD5 hash of the working key
    decDigest = hashlib.md5()
    decDigest.update(workingKey.encode('utf-8'))  # Convert workingKey to bytes
    
    # Convert hex back to bytes and decrypt
    encryptedText = unhexlify(cipherText)
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
    
    decryptedText = dec_cipher.decrypt(encryptedText).decode('utf-8')
    
    # Remove padding
    pad_length = ord(decryptedText[-1])
    decryptedText = decryptedText[:-pad_length]
    
    return decryptedText
