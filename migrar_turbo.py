import io
import pandas as pd
import os
from sqlalchemy import inspect, text
from dotenv import load_dotenv
from conexion import get_engine

load_dotenv()

"""
🚀 Módulo: migrar_turbo.py
RESPONSABILIDAD:
    1. Crea un esquema en la nube con el mismo nombre que tu base local.
    2. Migra las tablas DENTRO de ese esquema usando Turbo COPY.
"""

def obtener_tablas_locales(nombre_base_local):
    print(f"🔍 Inspeccionando base de datos local: '{nombre_base_local}'...")
    try:
        engine = get_engine(nombre_base_datos=nombre_base_local, env_force="local")
        inspector = inspect(engine)
        # Filtramos solo tablas reales del esquema public
        tablas = inspector.get_table_names(schema='public')
        print(f"📋 Tablas encontradas ({len(tablas)}): {tablas}")
        return tablas
    except Exception as e:
        print(f"❌ Error inspeccionando la base local: {e}")
        return []

def crear_esquema_si_no_existe(nombre_esquema, engine_nube):
    """
    Crea la 'carpeta' (Schema) en Supabase para guardar las tablas ordenadas.
    """
    nombre_esquema = nombre_esquema.lower() # Siempre minúsculas en Postgres
    print(f"   📂 Verificando/Creando esquema destino: '{nombre_esquema}'...")
    
    try:
        with engine_nube.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {nombre_esquema}"))
            conn.commit()
            print(f"      ✅ Esquema '{nombre_esquema}' listo.")
    except Exception as e:
        print(f"      ❌ Error creando esquema: {e}")

def copiar_estructura_tabla(nombre_tabla, nombre_esquema, engine_local, engine_nube):
    print(f"   🏗️ Creando estructura de: '{nombre_esquema}.{nombre_tabla}'...")
    
    # Leemos estructura local
    query = f"SELECT * FROM public.\"{nombre_tabla}\" LIMIT 0"
    df_estructura = pd.read_sql(query, engine_local)
    
    # LOAD: Usamos el parámetro 'schema' para apuntar a la carpeta correcta
    df_estructura.to_sql(
        name=nombre_tabla.lower(),
        con=engine_nube,
        schema=nombre_esquema.lower(), # <--- AQUÍ ESTÁ LA MAGIA
        if_exists='replace',
        index=False
    )

def copiar_datos_turbo(nombre_tabla, nombre_esquema, engine_local, engine_nube):
    conn_local = engine_local.raw_connection()
    conn_nube = engine_nube.raw_connection()
    
    esquema_dest = nombre_esquema.lower()
    tabla_dest = nombre_tabla.lower()
    
    try:
        cur_local = conn_local.cursor()
        cur_nube = conn_nube.cursor()
        buffer = io.StringIO()
        
        print(f"   ⬇️ Descargando datos (COPY)...")
        copy_to_sql = f"COPY (SELECT * FROM public.\"{nombre_tabla}\") TO STDOUT WITH CSV HEADER"
        cur_local.copy_expert(copy_to_sql, buffer)
        
        buffer.seek(0)
        
        print(f"   ⬆️ Subiendo a '{esquema_dest}.{tabla_dest}'...")
        # LOAD: Especificamos el esquema en el destino
        copy_from_sql = f"COPY {esquema_dest}.{tabla_dest} FROM STDIN WITH CSV HEADER"
        cur_nube.copy_expert(copy_from_sql, buffer)
        
        conn_nube.commit()
        print(f"   ✅ ¡Transferencia completada!")

    except Exception as e:
        conn_nube.rollback()
        print(f"   ❌ Error en COPY: {e}")
    finally:
        cur_local.close()
        cur_nube.close()
        conn_local.close()
        conn_nube.close()

def ejecutar_migracion_turbo():
    # 1. Configuración
    nombre_base = os.getenv('LOCAL_DB_TO_MIGRATE')
    if not nombre_base:
        print("🛑 ERROR: Define 'LOCAL_DB_TO_MIGRATE' en .env")
        return

    print(f"🚀 --- MIGRACIÓN A ESQUEMA PROPIO: {nombre_base.upper()} ---")
    
    lista_tablas = obtener_tablas_locales(nombre_base)
    if not lista_tablas: return

    # 2. Motores
    engine_local = get_engine(nombre_base_datos=nombre_base, env_force="local")
    engine_nube = get_engine(env_force="supabase")
    
    # 3. Crear el esquema (carpeta) una sola vez antes de empezar
    crear_esquema_si_no_existe(nombre_base, engine_nube)
    
    # 4. Bucle
    for tabla in lista_tablas:
        print(f"\n⚡ Procesando: {tabla}")
        try:
            # Ahora pasamos el nombre de la base como nombre del esquema
            copiar_estructura_tabla(tabla, nombre_base, engine_local, engine_nube)
            copiar_datos_turbo(tabla, nombre_base, engine_local, engine_nube)
        except Exception as e:
            print(f"   ❌ Error general: {e}")
            continue

    print(f"\n✨ --- FIN DEL PROCESO ---")

if __name__ == "__main__":
    ejecutar_migracion_turbo()