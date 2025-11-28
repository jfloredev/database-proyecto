import psycopg2
from psycopg2 import sql

# Conectar a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="db_mifarma",
    user="postgres",
    password="12345678"
)

cur = conn.cursor()

# Obtener todas las tablas
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cur.fetchall()
print("=== TABLAS EN LA BASE DE DATOS ===")
for table in tables:
    print(f"\n📋 Tabla: {table[0]}")
    
    # Obtener columnas de cada tabla
    cur.execute("""
        SELECT 
            column_name, 
            data_type, 
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table[0],))
    
    columns = cur.fetchall()
    for col in columns:
        nullable = "NULL" if col[2] == "YES" else "NOT NULL"
        default = f" DEFAULT {col[3]}" if col[3] else ""
        print(f"  - {col[0]}: {col[1]} {nullable}{default}")

cur.close()
conn.close()
