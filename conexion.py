import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

"""
🔌 Módulo: conexion.py

NIVEL: Core
RESPONSABILIDAD PRINCIPAL:
    Gestionar la conexión segura a la base de datos PostgreSQL.
    Este módulo abstrae el manejo de credenciales, leyéndolas exclusivamente
    del archivo de variables de entorno (.env) para evitar exponerlas
    en el código fuente (hardcodeo).

DEPENDENCIAS:
    - os, sqlalchemy, dotenv.
    - Requiere que el archivo '.env' esté presente en la raíz del proyecto.

FUNCIÓN PRINCIPAL: get_engine(nombre_base_datos=None)
    Crea y devuelve un objeto SQLAlchemy Engine.

    Args:
        nombre_base_datos (str): Nombre de la base de datos a la que se desea
                                 conectar. Si es nulo (None), se conecta a la
                                 base de datos por defecto configurada en .env.

    Raises:
        ValueError: Si la variable 'DB_PASS' no se encuentra en el entorno,
                    indicando una configuración incompleta de seguridad.

USO EN OTROS MÓDULOS:
    - La función 'get_engine' debe ser importada por cualquier script que
      necesite interactuar con la base de datos (Ej: 'ver_bases.py', etc.).

EJEMPLO:
    # Para usar la base por defecto:
    # engine = get_engine()

    # Para usar una base específica:
    # engine = get_engine("mi_otra_base")
"""

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Leer las credenciales comunes
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME_DEFAULT = os.getenv('DB_NAME') # La base de datos "por defecto"

def get_engine(nombre_base_datos=None):
    """
    Crea el motor de conexión.
    
    Args:
        nombre_base_datos (str): Opcional. Si lo escribes, conecta a esa base.
                                 Si lo dejas vacío, usa la del archivo .env.
    """
    
    # Verificación de seguridad
    if not DB_PASS:
        raise ValueError("Error: No se encontró la contraseña en el archivo .env")
        
    # Lógica de decisión: ¿Qué base de datos usamos?
    if nombre_base_datos:
        base_objetivo = nombre_base_datos
    else:
        base_objetivo = DB_NAME_DEFAULT

    # Creamos la cadena de conexión con la base elegida
    connection_string = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{base_objetivo}"
    
    engine = create_engine(connection_string)
    return engine

if __name__ == "__main__":
    # Prueba rápida
    try:
        engine = get_engine() # Probamos la conexión por defecto
        with engine.connect() as conn:
            print(f"✅ Conexión exitosa a la base por defecto: {DB_NAME_DEFAULT}")
    except Exception as e:
        print(f"❌ Error: {e}")