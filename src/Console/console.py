import sys
sys.path.append("src")

from MTO.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError

def main():
    while True:
        print("\nMenú:")
        print("1. Encriptar mensaje")
        print("2. Desencriptar mensaje")
        print("3. Salir")
        
        choice = input("Seleccione una opción: ")

        if choice == "1":
            try:
                message = input("Introduzca el mensaje a encriptar: ")
                password = input("Introduzca la contraseña: ")
                encrypted_message = encrypt_message(message, password)
                print("Mensaje encriptado:", encrypted_message)
            except EncryptionError as e:
                print(e)
        elif choice == "2":
            try:
                ciphertext = input("Introduzca el mensaje encriptado: ")
                password = input("Introduzca la contraseña: ")
                decrypted_message = decrypt_message(ciphertext, password)
                print("Mensaje desencriptado:", decrypted_message)
            except DecryptionError as e:
                print("Error al desencriptar el mensaje:", e)
        elif choice == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
