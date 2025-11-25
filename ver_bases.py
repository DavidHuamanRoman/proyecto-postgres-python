import pandas as pd
from conexion import get_engine

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