import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from conexion import get_engine

"""
⚙️ Módulo: inspector_avanzado.py

NIVEL: Engineering (Eng)
RESPONSABILIDAD:
    Utiliza el SQLAlchemy Inspector para realizar una auditoría completa del
    esquema de una base de datos PostgreSQL específica (definida por NOMBRE_BD).
    Este script está diseñado para detectar y reportar:
    1. Las columnas y sus tipos de datos.
    2. Las restricciones de Clave Primaria (Primary Key - PK).
    3. Las Claves Foráneas (Foreign Keys - FK) y las relaciones que definen.

USO:
    1. Asegúrese de que el archivo '.env' esté configurado correctamente.
    2. Ejecute el script directamente desde la terminal:
       $ python inspector_avanzado.py

CONFIGURACIÓN:
    Requiere que la función 'get_engine' esté disponible en 'conexion.py'.
    La variable NOMBRE_BD debe ser actualizada si se audita una base diferente
    a la predeterminada (retaildw).

SALIDA:
    Imprime en la consola un reporte estructurado y legible con los detalles
    técnicos de cada tabla encontrada en el esquema 'public'.
"""

# --- CONFIGURACIÓN ---
# 1. Definimos el nombre en una variable para usarlo en la conexión Y en el título
load_dotenv()

NOMBRE_BD = os.getenv("NOMBRE_BD_AUDITORIA", "postgres")

# 2. Conectamos usando esa variable
engine = get_engine(NOMBRE_BD)

def auditar_base_datos():
    inspector = inspect(engine)
    
    tablas = inspector.get_table_names(schema='public')
    
    # --- AQUÍ ESTÁ EL CAMBIO ---
    # Usamos la variable NOMBRE_BD y la ponemos en mayúsculas con .upper()
    print(f"\n🔎 AUDITORÍA TÉCNICA DE LA BASE DE DATOS: {NOMBRE_BD.upper()}")
    print("=" * 50) # He subido a 50 para que la línea sea más larga
    print(f"Total de tablas encontradas: {len(tablas)}\n")
    
    for tabla in tablas:
        print(f"📦 TABLA: {tabla}")
        # Aquí también usamos el truco del 40 (o 30 en este caso) para subrayar el nombre
        print("-" * 30) 
        
        # A. COLUMNAS
        columnas = inspector.get_columns(tabla, schema='public')
        print("   📂 Columnas:")
        for col in columnas:
            estado_nulo = "Opcional" if col['nullable'] else "Obligatorio"
            print(f"      - {col['name']} ({col['type']}) -> {estado_nulo}")

        # B. CLAVE PRIMARIA
        pk = inspector.get_pk_constraint(tabla, schema='public')
        if pk and pk['constrained_columns']:
            print(f"\n   🔑 Primary Key: {pk['constrained_columns']}")

        # C. CLAVES FORÁNEAS
        fks = inspector.get_foreign_keys(tabla, schema='public')
        if fks:
            print("\n   🔗 Relaciones (Foreign Keys):")
            for fk in fks:
                origen = fk['constrained_columns'][0]
                destino_tabla = fk['referred_table']
                destino_col = fk['referred_columns'][0]
                print(f"      - {origen} --> apunta a --> {destino_tabla}.{destino_col}")
        
        print("\n")

if __name__ == "__main__":
    try:
        auditar_base_datos()
    except Exception as e:
        print(f"❌ Error durante la auditoría: {e}")
        print(f"💡 Verifica que la base de datos '{NOMBRE_BD}' exista realmente.")