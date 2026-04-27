"""
ai_secure_data_handler.py

This module provides secure encryption and decryption functionalities for handling sensitive data 
within the G.O.D Framework. It ensures data confidentiality and integrity using the Fernet symmetric 
encryption scheme, compliant with modern security standards such as GDPR, HIPAA, and CCPA.

Author: G.O.D Framework Team (Open Source Contributors)
License: MIT License
Version: 1.0.0
"""

from cryptography.fernet import Fernet
import logging


class SecureDataHandler:
    """
    SecureDataHandler provides encryption and decryption functionality using
    the Fernet symmetric encryption scheme. It is designed to securely manage
    sensitive data by encoding plaintext into secure ciphertext and vice versa.
    The class can either generate a new encryption key or accept an existing
    one to ensure flexible usage in diverse security contexts.

    :ivar key: The encryption key used by the handler.
    :type key: bytes
    :ivar cipher: The Fernet cipher instance used for encryption and decryption.
    :type cipher: cryptography.fernet.Fernet
    """

    def __init__(self, encryption_key: bytes = None):
        """
        Initializes the SecureDataHandler. Generates a new encryption key
        if none is provided.

        Args:
            encryption_key (bytes, optional): An optional encryption key for
                                              creating a cipher instance.
        """
        if encryption_key is None:
            encryption_key = Fernet.generate_key()
            logging.info("Generated a new encryption key.")
        else:
            logging.info("Using an existing encryption key.")

        self.key = encryption_key
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> bytes:
        """
        Encrypts plaintext using the Fernet encryption scheme.

        Args:
            plaintext (str): The plaintext string to encrypt.

        Returns:
            bytes: The encrypted ciphertext.
        """
        try:
            encrypted = self.cipher.encrypt(plaintext.encode("utf-8"))
            logging.info("Encryption successful.")
            return encrypted
        except Exception as e:
            logging.error(f"Error encrypting data: {e}")
            return None

    def decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypts the given ciphertext using the Fernet encryption scheme.

        Args:
            ciphertext (bytes): The encrypted data to decrypt.

        Returns:
            str: The decrypted plaintext string.
        """
        try:
            decrypted = self.cipher.decrypt(ciphertext).decode("utf-8")
            logging.info("Decryption successful.")
            return decrypted
        except Exception as e:
            logging.error(f"Error decrypting data: {e}")
            return None

    def get_encryption_key(self) -> bytes:
        """
        Retrieves the encryption key being used by the handler.

        Returns:
            bytes: The encryption key.
        """
        return self.key


# Example Usage
if __name__ == "__main__":
    # Setup logging configuration
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Initialize SecureDataHandler with a dynamically generated key
    secure_handler = SecureDataHandler()

    # Encryption example
    sensitive_data = "Sensitive client information"
    encrypted_text = secure_handler.encrypt(sensitive_data)
    print(f"Encrypted: {encrypted_text}")

    # Decryption example
    decrypted_text = secure_handler.decrypt(encrypted_text)
    print(f"Decrypted: {decrypted_text}")

    # Retrieve encryption key (example for reusing keys in a secure manner)
    encryption_key = secure_handler.get_encryption_key()
    print(f"Encryption Key: {encryption_key}")