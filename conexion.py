import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

"""
🔌 Módulo: conexion.py

NIVEL: Core
RESPONSABILIDAD PRINCIPAL:
    Gestionar la conexión segura a la base de datos PostgreSQL.
    Implementa lógica "Multi-entorno" para alternar entre desarrollo local
    y producción (Supabase) sin cambiar el código, solo mediante configuración.

DEPENDENCIAS:
    - os, sqlalchemy, dotenv.
    - Requiere archivo '.env' con variable 'ENV' ('local' o 'supabase').

FUNCIÓN PRINCIPAL: get_engine(nombre_base_datos=None)
    Crea y devuelve un objeto SQLAlchemy Engine según el entorno activo.

    Args:
        nombre_base_datos (str): Opcional. Sobrescribe la base de datos destino.
                                 Útil en local si tienes múltiples bases.
                                 En Supabase, usualmente se mantiene la default 'postgres'.

    Raises:
        ValueError: Si faltan credenciales críticas para el entorno seleccionado.
"""

# 1. Cargar las variables del archivo .env
load_dotenv()

def get_engine(nombre_base_datos=None):
    """
    Crea el motor de conexión usando el driver psycopg2 (más estable).
    """
    load_dotenv() # Aseguramos cargar las variables
    
    modo_entorno = os.getenv('ENV', 'local').lower()
    args_conexion = {}

    if modo_entorno == 'supabase':
        user = os.getenv('SUPABASE_USER')
        password = os.getenv('SUPABASE_PASS')
        host = os.getenv('SUPABASE_HOST')
        port = os.getenv('SUPABASE_PORT')
        db_name_default = os.getenv('SUPABASE_NAME')
        prefix_log = "☁️ [NUBE] Supabase"
        
        # SSL obligatorio para Supabase
        args_conexion = {"sslmode": "require"}
        
    else:
        user = os.getenv('LOCAL_USER')
        password = os.getenv('LOCAL_PASS')
        host = os.getenv('LOCAL_HOST')
        port = os.getenv('LOCAL_PORT')
        db_name_default = os.getenv('LOCAL_NAME')
        prefix_log = "💻 [LOCAL] PC"

    if not password or not user or not host:
        raise ValueError(f"❌ Error: Faltan credenciales para {modo_entorno}")

    base_objetivo = nombre_base_datos if nombre_base_datos else db_name_default

    # CAMBIO IMPORTANTE: Usamos 'postgresql+psycopg2' en lugar de 'psycopg'
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{base_objetivo}"
    
    # Creamos el engine con un timeout de conexión para que no se cuelgue eternamente
    engine = create_engine(
        connection_string, 
        connect_args=args_conexion,
        pool_pre_ping=True # Verifica que la conexión esté viva antes de usarla
    )
    
    return engine

if __name__ == "__main__":
    # Prueba rápida de conexión al ejecutar este archivo directamente
    try:
        engine = get_engine()
        modo = os.getenv('ENV', 'local').upper()
        with engine.connect() as conn:
            print(f"✅ ¡ÉXITO! Conectado correctamente al entorno: {modo}")
    except Exception as e:
        print(f"❌ FALLO DE CONEXIÓN: {e}")