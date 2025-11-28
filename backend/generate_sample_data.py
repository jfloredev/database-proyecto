import psycopg2
from faker import Faker
import random

fake = Faker('es_ES')

DB_CONFIG = {
    'host': 'localhost',
    'database': 'db_mifarma',
    'user': 'postgres',
    'password': '12345678'
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def generate_sample_data():
    """Genera datos de muestra simples"""
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        print("🚀 Generando datos de muestra...")
        
        # 1. Crear algunos usuarios
        print("📝 Insertando usuarios...")
        usuarios = []
        for i in range(20):
            dni = f"{random.randint(10000000, 99999999)}"
            nombre = fake.first_name()
            apellido = fake.last_name()
            telefono = fake.phone_number()[:15]
            email = fake.email()
            fecha_registro = fake.date_between(start_date='-2y', end_date='today')
            
            cur.execute("""
                INSERT INTO usuario (dni, nombre, apellido, telefono, email, fecha_registro)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (dni, nombre, apellido, telefono, email, fecha_registro))
            usuarios.append(dni)
        
        # 2. Crear sedes
        print("🏢 Insertando sedes...")
        sedes = []
        for i in range(5):
            direccion = f"Av. Principal {100 + i}"
            nombre = f"MiFarma Sede {i+1}"
            cantidad_empleados = random.randint(5, 15)
            
            cur.execute("""
                INSERT INTO sede (direccion, nombre, cantidad_empleados)
                VALUES (%s, %s, %s)
                ON CONFLICT (direccion) DO NOTHING
            """, (direccion, nombre, cantidad_empleados))
            sedes.append(direccion)
        
        # 3. Crear medicamentos
        print("💊 Insertando medicamentos...")
        medicamentos_datos = [
            ("Paracetamol 500mg", "Bayer", 12.50, False),
            ("Ibuprofeno 400mg", "Pfizer", 15.00, False),
            ("Amoxicilina 500mg", "GSK", 25.00, True),
            ("Omeprazol 20mg", "Abbott", 30.00, True),
            ("Aspirina 100mg", "Bayer", 8.50, False),
            ("Loratadina 10mg", "Novartis", 18.00, False),
            ("Captopril 25mg", "Roche", 22.00, True),
            ("Metformina 850mg", "Merck", 35.00, True),
            ("Diclofenaco 50mg", "Sanofi", 20.00, False),
            ("Ciprofloxacino 500mg", "GSK", 28.00, True)
        ]
        
        medicamento_ids = []
        for i, med in enumerate(medicamentos_datos, 1):
            cur.execute("""
                INSERT INTO medicamento (id, nombre, marca, precio, necesita_receta)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (i, med[0], med[1], med[2], med[3]))
            medicamento_ids.append(i)
        
        # 4. Crear clientes (primeros 15 usuarios)
        print("👥 Insertando clientes...")
        clientes_creados = []
        for i, dni in enumerate(usuarios[:15], 1):
            direccion = f"Calle {fake.street_name()[:20]} {random.randint(100, 500)}"
            cur.execute("""
                INSERT INTO cliente (id, direccion, dni_usuario)
                VALUES (%s, %s, %s)
            """, (i, direccion, dni))
            clientes_creados.append({"id": i, "dni": dni})
        
        # 5. Crear empleados (últimos 5 usuarios)
        print("👨‍💼 Insertando empleados...")
        for i, dni in enumerate(usuarios[15:], 1):
            sede_direccion = random.choice(sedes)
            sueldo = round(random.uniform(1200, 2500), 2)
            fecha_contratacion = fake.date_between(start_date='-2y', end_date='today')
            turno = random.choice(["Mañana", "Tarde", "Noche"])
            estado = "Activo"
            
            cur.execute("""
                INSERT INTO empleado (id, dni_usuario, direccion_sede, sueldo, fecha_contratacion, turno, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (i, dni, sede_direccion, sueldo, fecha_contratacion, turno, estado))

        # 6. Crear monedero para cada cliente
        print("💳 Insertando monederos...")
        # Calcular id inicial para monedero
        cur.execute("SELECT COALESCE(MAX(id), 0) FROM monedero")
        start_id = (cur.fetchone() or [0])[0] + 1
        monederos_creados = 0
        for idx, c in enumerate(clientes_creados):
            monedero_id = start_id + idx
            saldo = round(random.uniform(0, 300), 2)
            ahorro_acumulado = round(random.uniform(0, 600), 2)
            fecha_creacion = fake.date_between(start_date='-2y', end_date='today')
            estado = random.choice([True, True, True, False])  # Mayoría activos
            cur.execute(
                """
                INSERT INTO monedero (id, dni_cliente, saldo, fecha_creacion, ahorro_acumulado, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (monedero_id, c["dni"], saldo, fecha_creacion, ahorro_acumulado, estado)
            )
            monederos_creados += 1
        
        conn.commit()
        
        print("✅ ¡Datos de muestra insertados exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - {len(usuarios)} usuarios")
        print(f"   - {len(sedes)} sedes")
        print(f"   - {len(medicamento_ids)} medicamentos")
        print(f"   - 15 clientes")
        print(f"   - 5 empleados")
        print(f"   - {monederos_creados} monederos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    generate_sample_data()