import pandas as pd
import os
from dotenv import load_dotenv
from conexion import get_engine

# Cargamos variables para poder leer etiquetas como 'SUPABASE_ACTIVE_PROJECT'
load_dotenv()

"""
🌍 Módulo: ver_bases.py
NIVEL: Server
"""

def listar_bases_datos():
    # 1. Obtenemos el motor de conexión
    engine = get_engine("postgres")
    
    # 2. INTELIGENCIA DE SERVIDOR: Detectamos a dónde estamos conectados
    # engine.url.host nos da la dirección real (IP o Dominio)
    host_real = engine.url.host
    
    # Leemos la configuración para darle un nombre amigable
    modo = os.getenv('ENV', 'local').upper()
    
    if modo == 'SUPABASE':
        proyecto_activo = os.getenv('SUPABASE_ACTIVE_PROJECT', 'DESCONOCIDO')
        etiqueta_servidor = f"NUBE: {proyecto_activo} ({host_real})"
    else:
        etiqueta_servidor = f"LOCAL PC ({host_real})"

    # Consulta al catálogo del sistema
    query = """
    SELECT datname as "Nombre Base de Datos", 
           pg_size_pretty(pg_database_size(datname)) as "Tamaño"
    FROM pg_database
    WHERE datistemplate = false
    ORDER BY datname;
    """
    
    try:
        df = pd.read_sql(query, engine)
        
        # 3. IMPRESIÓN DINÁMICA DEL TÍTULO
        print(f"\n--- 🌍 BASES DE DATOS EN: [ {etiqueta_servidor} ] ---")
        print(df)
        
    except Exception as e:
        print("❌ Error listando bases de datos:", e)

if __name__ == "__main__":
    listar_bases_datos()