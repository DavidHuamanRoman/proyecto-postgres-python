import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

"""
🔌 Módulo: conexion.py
RESPONSABILIDAD:
    Gestiona conexiones a Localhost y permite cambiar entre 
    múltiples proyectos de Supabase cambiando una sola variable en .env.
"""

load_dotenv()

def get_engine(nombre_base_datos=None, env_force=None):
    
    # 1. DECISIÓN DE ENTORNO
    if env_force:
        modo_entorno = env_force.lower()
    else:
        modo_entorno = os.getenv('ENV', 'local').lower()
    
    args_conexion = {}

    # 2. CONFIGURACIÓN DINÁMICA
    if modo_entorno == 'supabase':
        # Leemos qué proyecto está activo (PROYECTO1, PROYECTO2, etc.)
        prefijo = os.getenv('SUPABASE_ACTIVE_PROJECT', 'PROYECTO1').upper()
        
        # Construimos las variables dinámicamente:
        # Ej: Busca 'PROYECTO1_USER', 'PROYECTO1_PASS'...
        user = os.getenv(f'{prefijo}_USER')
        password = os.getenv(f'{prefijo}_PASS')
        host = os.getenv(f'{prefijo}_HOST')
        port = os.getenv(f'{prefijo}_PORT')
        db_name_default = os.getenv(f'{prefijo}_DB')
        
        # Validación específica para evitar errores si el prefijo está mal
        if not host:
            raise ValueError(f"❌ No se encontraron credenciales para el perfil: {prefijo} en .env")

        # SSL obligatorio
        args_conexion = {"sslmode": "require"}
        
    else:
        # Modo Local (Sin cambios)
        user = os.getenv('LOCAL_USER')
        password = os.getenv('LOCAL_PASS')
        host = os.getenv('LOCAL_HOST')
        port = os.getenv('LOCAL_PORT')
        db_name_default = os.getenv('LOCAL_NAME')

    # 3. VALIDACIÓN GENERAL
    if not password or not user:
        raise ValueError(f"❌ Error: Faltan credenciales para entorno {modo_entorno}")

    base_objetivo = nombre_base_datos if nombre_base_datos else db_name_default

    # 4. CONEXIÓN (Driver psycopg2)
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{base_objetivo}"
    
    engine = create_engine(
        connection_string, 
        connect_args=args_conexion,
        pool_pre_ping=True
    )
    
    return engine

# --- DIAGNÓSTICO ---
if __name__ == "__main__":
    print("\n🚦 INICIANDO DIAGNÓSTICO MULTI-PROYECTO...\n")
    try:
        # Prueba Nube (Detectará el proyecto activo)
        prefijo_actual = os.getenv('SUPABASE_ACTIVE_PROJECT', 'UNKNOWN')
        print(f"3️⃣  Probando conexión a SUPABASE (Perfil Activo: {prefijo_actual})...")
        
        engine_nube = get_engine(env_force="supabase")
        with engine_nube.connect() as conn:
            print(f"   ✅ ÉXITO. Conectado al servidor: {engine_nube.url.host}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")