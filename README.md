# Motor de Encriptación

Este proyecto es un motor de encriptación desarrollado en Python que utiliza el algoritmo AES (Rijindael). Su propósito es permitir a los usuarios encriptar y desencriptar mensajes utilizando contraseñas proporcionadas.

## Autores

Este maravilloso código fue creado por:

- Santiago Gutierrez Correa
- Eritz Sanchez Mena

## Métodos de Encriptación y Desencriptación

El método de encriptación utilizado es AES (Rijindael), un algoritmo de cifrado simétrico ampliamente utilizado en la actualidad debido a su seguridad y eficiencia.


### Estructura Sugerida

- **Carpeta Controller**: Contiene el código que conecta las bases de datos con la lógica de la aplicación.
  - `UserController.py`: Módulo en el que se encuentran todas las funciones que hace el programa con las bases de datos.

- **Carpeta Model**: Contiene el código fuente de la lógica de la aplicación.
  - `MTO.py`: Módulo principal que proporciona funciones para encriptar y desencriptar mensajes.
  - `SecretConfig.py`: Módulo con los datos de conexión a la base de datos.

- **Carpeta View**: Contiene el código que interactua con el usuario.
  - `console.py`: Módulo con la estructura del main para correr el código.
  - `Interface.py`: Módulo con toda la lógica visual para correr el programa.

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

### Casos de prueba de bases de datos

#### Normales
1. Crear tablas
2. Insertar datos
3. Actualizar datos en una tabla
4. Hacer consultas en la tabla

#### Error
1. Falla al crear una tabla
2. Registro no existente
3. Insercción sin dato obligatorio
4. Error al buscar nombre no existente en la base de datos

## ¿Cómo lo hago funcionar?

- **Prerrequisitos**: 
  - Python 3.x instalado en su sistema.
  - Bibliotecas de Python necesarias, que se pueden instalar mediante pip de la siguiente manera: solo copia los comandos que te dejaremos a continuación en tu consola dale enter y listo(cryptography, kivy).
    
    -`pip install cryptography`
    
    -`pip install kivy`

    -`pip install psycopg2-binary`


- **Ejecución**: 
  - Clona este repositorio en tu máquina local.
  - Pega esta ruta en tu consola.
  
     -Para correr la consola del programa: `python src\Console\console.py`
    
     -Para correr la interfaz del programa: `python src\Interface\MTO-gui.py`

      -Para correr las pruebas unitarias del programa: `python test\test.py`
  
**Nota:** Para usar las opciones de las bases de datos deberas crear tu propia base de datos en Neon tech, y pegar las credencial en el archivo de `SecretConfig.py`

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún error o tienes alguna sugerencia de mejora, no dudes en abrir un *issue* o enviar un *pull request*.

