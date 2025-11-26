import pandas as pd
from conexion import get_engine

"""
🌍 Módulo: ver_bases.py

NIVEL: Server
RESPONSABILIDAD PRINCIPAL:
    Se conecta a la base de datos "maestra" o por defecto ('postgres' o la
    definida en .env) para consultar el catálogo del sistema. Su objetivo es
    listar todas las bases de datos existentes en el servidor y reportar su
    tamaño en disco de forma legible.

DEPENDENCIAS:
    - pandas (para generar la salida tabular).
    - from conexion import get_engine (para establecer la conexión segura).

FUNCIÓN PRINCIPAL: listar_bases_datos()
    Ejecuta una consulta SQL al catálogo 'pg_database'.

    Proceso:
        1. Utiliza get_engine() para conectar a la base de datos 'postgres'.
        2. Ejecuta una consulta SELECT que utiliza la función interna
           pg_database_size().
        3. Filtra las plantillas internas del sistema (datistemplate = false).
        4. Carga el resultado en un DataFrame de Pandas.

USO:
    Ejecutar directamente desde la terminal:
    $ python ver_bases.py

SALIDA:
    Imprime en la consola un DataFrame de Pandas con dos columnas:
    "Nombre Base de Datos" y "Tamaño".
"""

def listar_bases_datos():
    # Nos conectamos a la base por defecto para preguntar por las demás
    engine = get_engine("postgres")
    
    # Consulta al catálogo del sistema (filtra las plantillas/templates)
    query = """
    SELECT datname as "Nombre Base de Datos", 
           pg_size_pretty(pg_database_size(datname)) as "Tamaño"
    FROM pg_database
    WHERE datistemplate = false
    ORDER BY datname;
    """
    
    try:
        df = pd.read_sql(query, engine)
        print("\n--- 🌍 BASES DE DATOS EN TU SERVIDOR ---")
        print(df)
    except Exception as e:
        print("❌ Error listando bases de datos:", e)

if __name__ == "__main__":
    listar_bases_datos()