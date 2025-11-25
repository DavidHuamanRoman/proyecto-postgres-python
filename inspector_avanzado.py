from sqlalchemy import inspect
from conexion import get_engine

# --- CONFIGURACIÓN ---
# 1. Definimos el nombre en una variable para usarlo en la conexión Y en el título
NOMBRE_BD = "retaildw" 

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
    auditar_base_datos()