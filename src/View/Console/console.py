import sys
sys.path.append("src")

from Model.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError
from Controller import UserController as Us
def main():
    while True:
        print("\nMenú:")
        print("1. Encriptar mensaje")
        print("2. Desencriptar mensaje")
        print("3. Crear tabla")
        print("4. Borrar tabla")
        print("5. Insertar datos")
        print("6. Actualizar datos")
        print("7. Buscar por nombre")
        print("8. Salir")
        
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
            Us.CreateTable()
            print("Tabla creada (si no existía).")
        elif choice == "4":
            Us.DeleteTable()
            print("Tabla borrada.")
        elif choice == "5":
            name = input("Ingrese el nombre: ")
            password = input("Ingrese la contraseña: ")
            mensaje = input("Ingrese el mensaje: ")
            Us.InsertData(name, password, mensaje)
            print("Datos insertados.")
        elif choice == "6":
            name = input("Ingrese el nombre del usuario a actualizar: ")
            password = input("Ingrese la nueva contraseña: ")
            mensaje = input("Ingrese el nuevo mensaje: ")
            Us.UpdateTable(name, password, mensaje)
            print("Datos actualizados.")
        elif choice == "7":
            name = input("Ingrese el nombre a buscar: ")
            try:
                Us.SearchByName(name)
            except Us.ErrorNoEncontrado as e:
                print(e)
        elif choice == "8":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
