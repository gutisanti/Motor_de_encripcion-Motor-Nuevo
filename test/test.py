import unittest

import sys
sys.path.append("src")

from MTO.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError

class TestEncryption(unittest.TestCase):

    # Casos de prueba para encriptar mensajes normales
    def test_normal_encryption_current_key(self):
        # Caso de prueba para encriptar con una clave corriente
        message = "Hola Mundo"
        password = "password123"
        encrypted_message = encrypt_message(message, password)
        self.assertTrue(encrypted_message)

    def test_normal_encryption_number_message(self):
        # Caso de prueba para encriptar un mensaje con números
        message = "123456"
        password = "password123"
        encrypted_message = encrypt_message(message, password)
        self.assertTrue(encrypted_message)

    def test_normal_encryption_character_message(self):
        # Caso de prueba para encriptar un mensaje con caracteres especiales
        message = "!@#$%^&*()_+"
        password = "password123"
        encrypted_message = encrypt_message(message, password)
        self.assertTrue(encrypted_message)

    # Casos de prueba para errores de encriptación
    def test_error_minimun_characters_key(self):
        # Caso de prueba para una clave con menos de 4 caracteres
        entrance = "Hola Mundo"
        password = "123"  # Clave con solo 3 caracteres

        # Proceso de encriptación debería lanzar una excepción
        with self.assertRaises(EncryptionError):
            encrypt_message(entrance, password)
            
    def test_error_letter_key(self):
        # Caso de prueba para una clave con letras solamente
        message = "Hola Mundo"
        password = "abcdef"
        with self.assertRaises(EncryptionError):
            encrypt_message(message, password)

    def test_error_space_key(self):
        # Caso de prueba para una clave que contiene espacios
        message = "Hola Mundo"
        password = "abc def"
        with self.assertRaises(EncryptionError):
            encrypt_message(message, password)

    def test_error_special_characters_key(self):
        # Caso de prueba para una clave con solo caracteres especiales
        message = "Hola Mundo"
        password = "!@#$"
        with self.assertRaises(EncryptionError):
            encrypt_message(message, password)

    # Casos de prueba extraordinarios
    def test_extraordinary_empty_message(self):
        # Caso de prueba para encriptar un mensaje vacío
        message = ""
        password = "password123"
        with self.assertRaises(EncryptionError):
            encrypt_message(message, password)

    def test_extraordinary_emoji_message(self):
        # Caso de prueba para encriptar un mensaje con emojis
        message = "😊😊😊😊"
        password = "password123"
        encrypted_message = encrypt_message(message, password)
        self.assertTrue(encrypted_message)

    def test_extraordinary_sinogram_message(self):
        # Caso de prueba para encriptar un mensaje con sinogramas
        message = "汉字"
        password = "password123"
        encrypted_message = encrypt_message(message, password)
        self.assertTrue(encrypted_message)


class TestDecryption(unittest.TestCase):

    # Casos de prueba para desencriptar mensajes normales
    def test_normal_decryption_current_key(self):
        # Caso de prueba para desencriptar con una clave corriente
        encrypted_message = "SEjT3PCmuWUWxuK7vS8hQw=="
        password = "1234"
        decrypted_message = decrypt_message(encrypted_message, password)
        self.assertTrue(decrypted_message)

    def test_normal_decryption_number_message(self):
        # Caso de prueba para desencriptar un mensaje con números
        encrypted_message = "t9iLF8ieMOX4KFxhYz9tdQ=="
        password = "1234"
        decrypted_message = decrypt_message(encrypted_message, password)
        self.assertTrue(decrypted_message)

    def test_normal_decryption_character_message(self):
        # Caso de prueba para desencriptar un mensaje con caracteres especiales
        encrypted_message = "SEjT3PCmuWUWxuK7vS8hQw=="
        password = "1234"
        decrypted_message = decrypt_message(encrypted_message, password)
        self.assertTrue(decrypted_message)

    # Casos de prueba extraordinarios
    def test_extraordinary_empty_message(self):
        # Caso de prueba para desencriptar un mensaje vacío
        encrypted_message = ""
        password = "password123"
        with self.assertRaises(DecryptionError):
            decrypt_message(encrypted_message, password)

    def test_extraordinary_modified_message(self):
        # Caso de prueba para desencriptar un mensaje modificado
        encrypted_message = "SEjT3PCmuWUWxuK7vS8hQw=="
        password = "1234"
        decrypted_message = decrypt_message(encrypted_message, password)
        self.assertTrue(decrypted_message)

    def test_extraordinary_none_message(self):
        # Caso de prueba para desencriptar un mensaje None
        encrypted_message = None
        password = "password123"
        with self.assertRaises(DecryptionError):
            decrypt_message(encrypted_message, password)

    # Casos de prueba para errores de desencriptación
    def test_error_incorrect_key(self):
        # Caso de prueba para una clave incorrecta
        encrypted_message = "Mensaje encriptado"
        correct_password = "password123"
        incorrect_password = "incorrectpassword"
        with self.assertRaises(DecryptionError):
            decrypt_message(encrypted_message, incorrect_password)

    def test_error_unencrypted_message(self):
        # Caso de prueba para un mensaje no encriptado
        unencrypted_message = "Mensaje no encriptado"
        password = "password123"
        with self.assertRaises(DecryptionError):
            decrypt_message(unencrypted_message, password)

    def test_error_corrupt_message(self):
        # Caso de prueba para un mensaje encriptado corrupto
        corrupt_encrypted_message = "Mensaje encriptado corrupto"
        password = "password123"
        with self.assertRaises(DecryptionError):
            decrypt_message(corrupt_encrypted_message, password)

    def test_error_empty_key(self):
        # Caso de prueba para una clave vacía
        encrypted_message = "Mensaje encriptado"
        password = ""
        with self.assertRaises(DecryptionError):
            decrypt_message(encrypted_message, password)

if __name__ == '__main__':
    unittest.main()
