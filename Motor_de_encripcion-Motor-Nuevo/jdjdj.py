from MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError
try:
    # Llamamos a la función encrypt_message con una clave de menos de 4 caracteres
    encrypt_message("Hola Mundo", "abc")
    print("No se lanzó ninguna excepción")
except EncryptionError as e:
    print("Se lanzó una EncryptionError:", e)
except Exception as ex:
    print("Se lanzó una excepción diferente:", ex)
