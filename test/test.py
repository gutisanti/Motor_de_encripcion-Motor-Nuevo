import unittest
from unittest import TestCase, mock
import psycopg2
import sys
sys.path.append("src")
from Controller.UserController import GetCursor, CreateTable, DeleteTable, InsertData, UpdateTable, SearchByName, ErrorNoEncontrado, ErrorTableCreation
from Model.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError
from Model import SecretConfig as SecretConfig


class TestDataBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configuración inicial para la base de datos
        cls.conn = psycopg2.connect(
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD,
            host=SecretConfig.PGHOST,
            port=SecretConfig.PGPORT,
            sslmode='require'
        )
        cls.cursor = cls.conn.cursor()
        CreateTable()

    @classmethod
    def tearDownClass(cls):
        # Eliminar la tabla después de las pruebas
        DeleteTable()
        cls.conn.close()

    def setUp(self):
        # Reinicia la conexión y el cursor en caso de que se haya producido un error anteriormente
        self.conn.rollback()
        self.cursor = self.conn.cursor()

        # Elimina todos los registros de la tabla antes de cada prueba
        try:
            self.cursor.execute("DELETE FROM propietarios")
            self.conn.commit()  # Confirma la transacción para asegurarse de que el cambio se aplique
        except Exception as e:
            # Si ocurre algún error al eliminar los registros, imprime el error y revierte la transacción
            print("Error al eliminar registros:", e)
            self.conn.rollback()


    def test_insercion_correcta(self):
        # Caso Normal 1: Inserción Correcta de Datos
        try:
            InsertData('Juan Pérez', 'password123', 'mensaje secreto')
            self.cursor.execute("SELECT * FROM propietarios WHERE name = 'Juan Pérez'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Error: El registro no fue insertado correctamente.")
            self.assertEqual(result[1], 'Juan Pérez', "Error: El nombre del registro no coincide.")
            self.assertEqual(result[2], 'password123', "Error: La contraseña del registro no coincide.")
            self.assertEqual(decrypt_message(result[3], 'password123'), 'mensaje secreto', "Error: El mensaje encriptado no coincide.")
        except Exception as e:
            self.fail(f"Error inesperado durante la inserción: {e}")

    def test_actualizacion_correcta(self):
        # Caso Normal 2: Actualización Correcta de Datos
        try:
            InsertData('Maria Lopez', 'password123', 'mensaje secreto')
            UpdateTable('Maria Lopez', 'newpassword1', 'nuevo mensaje secreto')
            self.cursor.execute("SELECT password, mensajeencriptado FROM propietarios WHERE name = 'Maria Lopez'")
            result = self.cursor.fetchone()
            self.assertEqual(result[0], 'newpassword1', "Error: La contraseña no fue actualizada correctamente.")
            self.assertEqual(decrypt_message(result[1], 'newpassword1'), 'nuevo mensaje secreto', "Error: El mensaje no fue actualizado correctamente.")
        except Exception as e:
            self.fail(f"Error inesperado durante la actualización: {e}")

    def test_search_by_name_error(self):
        # Caso de Error: Búsqueda de un nombre que no existe en la base de datos
        with self.assertRaises(ErrorNoEncontrado, msg="No se lanzó la excepción ErrorNoEncontrado como se esperaba"):
            SearchByName("NombreInexistente")       

    def test_eliminacion_correcta(self):
        # Caso Normal 3: Eliminación Correcta de Datos
        try:
            InsertData('Carlos Ruiz', 'password123', 'mensaje secreto')
            self.cursor.execute("DELETE FROM propietarios WHERE name = 'Carlos Ruiz'")
            self.conn.commit()
            self.cursor.execute("SELECT * FROM propietarios WHERE name = 'Carlos Ruiz'")
            result = self.cursor.fetchone()
            self.assertIsNone(result, "Error: El registro no fue eliminado correctamente.")
        except Exception as e:
            self.fail(f"Error inesperado durante la eliminación: {e}")

    def test_consulta_correcta(self):
        # Caso Normal 4: Consulta Correcta de Datos
        try:
            InsertData('Ana Gomez', 'password123', 'mensaje secreto')
            resultados = SearchByName('Ana Gomez')
            self.assertGreater(len(resultados), 0, "Error: La consulta no devolvió los resultados esperados.")
            self.assertEqual(resultados[0]['nombre'], 'Ana Gomez', "Error: El nombre del resultado no coincide.")
            self.assertEqual(decrypt_message(resultados[0]['mensaje_encriptado'], 'password123'), 'mensaje secreto', "Error: El mensaje encriptado no coincide.")
        except ErrorNoEncontrado as e:
            self.fail(f"Error inesperado durante la consulta: {e}")

    
    def test_insercion_sin_dato_obligatorio(self):
        # Caso de Error : Inserción de Datos con Restricción de No Nulos
        with self.assertRaises(psycopg2.IntegrityError, msg="Error: La inserción sin dato obligatorio no lanzó IntegrityError como se esperaba."):
            self.cursor.execute("INSERT INTO propietarios (name, mensajeencriptado) VALUES (%s, %s)", (None, encrypt_message('mensaje', 'password123')))
            self.conn.commit()

    def test_actualizacion_registro_no_existente(self):
        # Caso de Error : Actualización de Registro No Existente
        UpdateTable('no.existe@example.com', 'password123', 'mensaje secreto')
        self.cursor.execute("SELECT * FROM propietarios WHERE name = 'no.existe@example.com'")
        result = self.cursor.fetchone()
        self.assertIsNone(result, "Error: Se esperaba que no existiera ningún registro con el nombre 'no.existe@example.com'.")

    def test_create_table_success(self):
        # Caso de normal: Creación de la tabla cuando no existe
        try:
            CreateTable()
        except psycopg2.Error as e:
            self.fail(f"Se produjo un error inesperado: {e}")

    # Caso de Error: Intento de creación de tabla cuando ya existe
    def test_create_table_failure(self):
        with mock.patch('Controller.UserController.GetCursor') as mock_get_cursor:
            mock_cursor = mock_get_cursor.return_value
            mock_cursor.execute.side_effect = Exception("Simulated error")

            with self.assertRaises(ErrorTableCreation, msg="No se lanzó la excepción ErrorTableCreation como se esperaba"):
                CreateTable()    
       

    
            
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


