
import sys
sys.path.append("src")

from Model.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError

import psycopg2
import Model.SecretConfig as SecretConfig

class ErrorNoEncontrado( Exception ):
    """ Excepcion que indica que una fila buscada no fue encontrada"""
    pass


def ObtenerCursor( ) :
    """
    Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    DATABASE = SecretConfig.PGDATABASE
    USER = SecretConfig.PGUSER
    PASSWORD = SecretConfig.PGPASSWORD
    HOST = SecretConfig.PGHOST
    PORT = SecretConfig.PGPORT
    try:
        connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT, sslmode = 'require')
        print("Conectado rey")
        return connection.cursor()
    except psycopg2.OperationalError as e:
        print("Nada manito")

def CrearTabla():
    """
    Crea la tabla de usuarios, en caso de que no exista
    """    


    cursor = ObtenerCursor()
    try:
        cursor.execute(""" create table prueba (
  cedula varchar( 20 )  NOT NULL,
  nombre text not null,
  apellido text not null,
  telefono varchar(20),
  correo text,
  direccion text not null,
  codigo_municipio varchar(40) not null,
  codigo_departamento varchar(40) NOT NULL
); 
""")
        cursor.connection.commit()
    except:
        # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
        cursor.connection.rollback()

def EliminarTabla():
    """
    Borra (DROP) la tabla en su totalidad
    """    
    sql = "drop table usuarios;"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    sql = "drop table familiares;"
    cursor.execute( sql )
    cursor.connection.commit()

ObtenerCursor()