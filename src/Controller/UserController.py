
import sys
sys.path.append("src")

from Model.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError

import psycopg2
import Model.SecretConfig as SecretConfig

class ErrorNoEncontrado( Exception ):
    """ Excepcion que indica que una fila buscada no fue encontrada"""
    pass


def GetCursor( ) :
    """
    Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    DATABASE = SecretConfig.PGDATABASE
    USER = SecretConfig.PGUSER
    PASSWORD = SecretConfig.PGPASSWORD
    HOST = SecretConfig.PGHOST
    PORT = SecretConfig.PGPORT
    
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT, sslmode = 'require')
    return connection.cursor()


def CreateTable():
    """
    Crea la tabla de usuarios, en caso de que no exista
    """    


    cursor = GetCursor()
    try:
        cursor.execute(""" create table propietarios (
id SERIAL PRIMARY KEY,  
name text not null,
  password text not null,
  mensajeEncriptado text not null
); 
""")
        
        cursor.connection.commit()
    except:
        # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
        cursor.connection.rollback()

def DeleteTable():
    """
    Borra (DROP) la tabla en su totalidad
    """    
    cursor = GetCursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS propietarios;")
        cursor.connection.commit()
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error borrando la tabla: {e}")

def InsertData(name,password,mensaje):
    """
    Agrega los datos de cada usuario en la tabla
    """
    try:
        cursor = GetCursor()
        cursor.execute(f"""
            insert into propietarios (
                name,  password,  mensajeencriptado
            )
            values 
            (
                '{name}', '{password}' , '{encrypt_message(mensaje,password)}'
            );
                        """)
            
        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes
        cursor.connection.commit()
    except  :
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar el usuario : ")

def UpdateTable(name,password,mensaje):
    """
    Actualiza los datos de un usuario en la base de datos

    """
    cursor = GetCursor()
    cursor.execute(f"""
        UPDATE propietarios
        SET password ='{password}', mensajeencriptado ='{encrypt_message(mensaje,password)}'
        WHERE name ='{name}';
    """)
    # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
    # pero si necesitan commit() para hacer los cambios persistentes
    cursor.connection.commit()

def SearchByName(name):
    """
    Busca los mensajes encriptados por cada usuario 
    """
    cursor = GetCursor()
    print("Conexión establecida")  # Depuración
    cursor.execute(f"""
        SELECT id,name, mensajeencriptado
        FROM propietarios
        WHERE name = '{name}';
    """)
    print("Consulta ejecutada")  # Depuración
    
    filas = cursor.fetchall()
    resultados = []
    
    for fila in filas:
        resultados.append({"id": fila[0],"nombre": fila[1], "mensaje_encriptado": fila[2]})

    if not resultados:
            raise ErrorNoEncontrado("No se encontraron registros para el nombre: " + name)
        
        # Imprimir todos los valores encontrados
    for resultado in resultados:
            print(f"ID: {resultado['id']}, Nombre: { resultado['nombre']}, Mensaje Encriptado: {resultado['mensaje_encriptado']}")

    return resultados

    


GetCursor()
CreateTable()

resultados = SearchByName("eritz")
