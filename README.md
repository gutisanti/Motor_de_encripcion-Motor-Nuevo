# Motor de Encriptación

Este proyecto es un motor de encriptación desarrollado en Python que utiliza el algoritmo AES (Rijindael). Su propósito es permitir a los usuarios encriptar y desencriptar mensajes utilizando contraseñas proporcionadas.

## Autores

Este maravilloso código fue creado por:

- Santiago Gutierrez Correa
- Eritz Sanchez Mena

## Métodos de Encriptación y Desencriptación

El método de encriptación utilizado es AES (Rijindael), un algoritmo de cifrado simétrico ampliamente utilizado en la actualidad debido a su seguridad y eficiencia.

### Estructura Sugerida

- **Carpeta src**: Contiene el código fuente de la lógica de la aplicación.
  - `MTO.py`: Módulo principal que proporciona funciones para encriptar y desencriptar mensajes.
- **Carpeta tests**: Contiene las pruebas unitarias para el código fuente.

Recuerde que cada carpeta de código fuente debe contener un archivo `__init__.py` que permite que Python reconozca la carpeta como un módulo y pueda hacer import.
### Estructura Sugerida

- **Carpeta src**: Contiene el código fuente de la lógica de la aplicación.
  - `MTO.py`: Módulo principal que proporciona funciones para encriptar y desencriptar mensajes.
- **Carpeta tests**: Contiene las pruebas unitarias para el código fuente.

Recuerde que cada carpeta de código fuente debe contener un archivo `__init__.py` que permite que Python reconozca la carpeta como un módulo y pueda hacer import.

## Casos de Prueba

### Encriptar

#### Normales
1. Clave_corriente
2. Mensaje_numero
3. Mensaje_caracteres

#### Error
1. Clave_caracteres_minimo
2. Clave_con_letra
3. Clave_con_espacios
4. Clave_caracteres

#### Extraordinarios
1. Mensaje_vacio
2. Mensaje_emojis
3. Mensaje_sinogramas

### Desencriptar

#### Normales
1. Clave_corriente
2. Mensaje_numero
3. Mensaje_caracteres

#### Extraordinario
1. Mensaje_vacio
2. Mensaje_modificado
3. Mensaje_none

#### Error
1. Clave_incorrecta
2. Mensaje_no_encriptado
3. Mensaje_corrupto
4. Clave_vacia

## ¿Cómo lo hago funcionar?

- **Prerrequisitos**: 
  - Python 3.x instalado en su sistema.
  - Bibliotecas de Python necesarias, que se pueden instalar mediante pip (por ejemplo, cryptography).

- **Ejecución**: 
  - Clona este repositorio en tu máquina local.
  - Importa el módulo `MTO` en tu script de Python.
  - Utiliza las funciones `encrypt_message()` y `decrypt_message()` proporcionadas por el módulo `MTO` para encriptar y desencriptar mensajes respectivamente.

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún error o tienes alguna sugerencia de mejora, no dudes en abrir un *issue* o enviar un *pull request*.

## Uso

Para ejecutar las pruebas unitarias, desde la carpeta src, use el siguiente comando:

```bash
cleancode-01\src> python -m unittest discover ..\tests -p '*test*.py'
