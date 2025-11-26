import pandas as pd
from conexion import get_engine

"""
📋 Módulo: mapear_db.py

NIVEL: Analysis
RESPONSABILIDAD PRINCIPAL:
    Generar un "Diccionario de Datos" legible para una base de datos específica.
    Este script se conecta a la base definida en la variable 'BASE_A_ANALIZAR'
    y extrae la estructura de todas las tablas en el esquema 'public'.

MÉTODO DE EXTRACCIÓN:
    Utiliza el 'information_schema' de PostgreSQL para consultar los nombres
    de las tablas y sus columnas/tipos de datos. Los resultados se formatean
    en DataFrames de Pandas para una presentación visual limpia.

DEPENDENCIAS:
    - pandas (para la extracción y el formato tabular).
    - from conexion import get_engine (para la conexión).

FUNCIÓN PRINCIPAL: obtener_diccionario_datos()
    Itera sobre las tablas y ejecuta una consulta detallada por cada una.

CONFIGURACIÓN REQUERIDA:
    La variable global 'BASE_A_ANALIZAR' debe ser ajustada manualmente dentro
    del script para apuntar a la base de datos objetivo.

USO:
    Ejecutar directamente desde la terminal:
    $ python mapear_db.py

SALIDA:
    Imprime en la consola un listado secuencial de todas las tablas,
    mostrando para cada una: el nombre de la columna y el tipo de dato.
"""

# --- CONFIGURACIÓN ---
# Aquí escribes la base que quieres investigar
BASE_A_ANALIZAR = "retaildw" 

# Creamos la conexión específica
print(f"🔌 Conectando a: {BASE_A_ANALIZAR}...")
try:
    engine = get_engine(BASE_A_ANALIZAR)
except Exception as e:
    print(f"❌ Error conectando a {BASE_A_ANALIZAR}: {e}")
    exit()

def obtener_diccionario_datos():
    """
    Genera un reporte completo de todas las tablas y sus columnas.
    """
    
    # 1. Obtenemos la lista de tablas
    query_tablas = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
    """
    try:
        df_tablas = pd.read_sql(query_tablas, engine)
        tablas = df_tablas['table_name'].tolist()
    except Exception as e:
        print("Error obteniendo tablas:", e)
        return

    if not tablas:
        print("⚠️ Esta base de datos está vacía (no tiene tablas en 'public').")
        return

    print(f"\n--- 📖 DICCIONARIO DE DATOS: {BASE_A_ANALIZAR.upper()} ---")
    print(f"Encontradas {len(tablas)} tablas.\n")

    # 2. Iteramos sobre cada tabla para mostrar su "receta" (columnas)
    for tabla in tablas:
        query_cols = f"""
        SELECT column_name as "Columna", 
               data_type as "Tipo Dato"
        FROM information_schema.columns
        WHERE table_name = '{tabla}'
        ORDER BY ordinal_position;
        """
        df_cols = pd.read_sql(query_cols, engine)
        
        # Formato visual para que sea fácil de leer
        print(f"🔹 TABLA: '{tabla}'")
        print("-" * 40)
        # Imprimimos el DataFrame sin el índice numérico para que se vea limpio
        print(df_cols.to_string(index=False)) 
        print("\n" + "="*40 + "\n") # Separador entre tablas

if __name__ == "__main__":
    obtener_diccionario_datos()