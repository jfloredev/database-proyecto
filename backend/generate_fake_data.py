import psycopg2
from faker import Faker
import random
from datetime import datetime, date, timedelta
from decimal import Decimal

fake = Faker('es_ES')  # Datos en español

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'database': 'db_mifarma',
    'user': 'postgres',
    'password': '12345678'
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def clear_tables():
    """Limpia todas las tablas en el orden correcto (respetando foreign keys)"""
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # Orden de eliminación respetando foreign keys
        tables = [
            'movimiento_monedero',
            'receta_incluye_medicamento', 
            'inventario_contiene_medicamento',
            'venta_tiene_medicamento',
            'receta_medica',
            'venta',
            'monedero',
            'inventario',
            'cliente',
            'empleado',
            'usuario',
            'medicamento',
            'sede'
        ]
        
        for table in tables:
            cur.execute(f"DELETE FROM {table}")
            print(f"✓ Limpiada tabla {table}")
        
        conn.commit()
        print("🧹 Todas las tablas han sido limpiadas")
        
    except Exception as e:
        print(f"❌ Error limpiando tablas: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def generate_users(num_users=100):
    """Genera usuarios"""
    conn = connect_db()
    cur = conn.cursor()
    
    users = []
    
    for _ in range(num_users):
        # Generar DNI peruano de 8 dígitos
        dni = f"{random.randint(10000000, 99999999)}"
        nombre = fake.first_name()
        apellido = fake.last_name()
        telefono = fake.phone_number()
        email = fake.email()
        fecha_registro = fake.date_between(start_date='-2y', end_date='today')
        
        users.append((dni, nombre, apellido, telefono, email, fecha_registro))
    
    try:
        cur.executemany("""
            INSERT INTO usuario (dni, nombre, apellido, telefono, email, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, users)
        
        conn.commit()
        print(f"✓ Insertados {num_users} usuarios")
        return [user[0] for user in users]  # Retorna lista de DNIs
        
    except Exception as e:
        print(f"❌ Error insertando usuarios: {e}")
        conn.rollback()
        return []
    finally:
        cur.close()
        conn.close()

def generate_sedes(num_sedes=10):
    """Genera sedes"""
    conn = connect_db()
    cur = conn.cursor()
    
    sedes = []
    
    for i in range(num_sedes):
        # Direcciones más cortas
        direccion = f"Av. {fake.street_name()[:15]} {random.randint(100, 999)}"
        nombre = f"MiFarma {i+1}"
        cantidad_empleados = random.randint(5, 20)
        
        sedes.append((direccion, nombre, cantidad_empleados))
    
    try:
        cur.executemany("""
            INSERT INTO sede (direccion, nombre, cantidad_empleados)
            VALUES (%s, %s, %s)
        """, sedes)
        
        conn.commit()
        print(f"✓ Insertadas {num_sedes} sedes")
        return [sede[0] for sede in sedes]  # Retorna lista de direcciones
        
    except Exception as e:
        print(f"❌ Error insertando sedes: {e}")
        conn.rollback()
        return []
    finally:
        cur.close()
        conn.close()

def generate_medicamentos(num_medicamentos=50):
    """Genera medicamentos"""
    conn = connect_db()
    cur = conn.cursor()
    
    medicamentos_nombres = [
        "Paracetamol", "Ibuprofeno", "Aspirina", "Omeprazol", "Amoxicilina",
        "Loratadina", "Diclofenaco", "Metamizol", "Captopril", "Metformina",
        "Atorvastatina", "Losartán", "Amlodipino", "Simvastatina", "Ranitidina",
        "Ciprofloxacino", "Azitromicina", "Prednisona", "Furosemida", "Digoxina"
    ]
    
    marcas = ["Bayer", "Pfizer", "Novartis", "GSK", "Abbott", "Roche", "Merck", "Sanofi"]
    
    medicamentos = []
    
    for i in range(num_medicamentos):
        nombre = random.choice(medicamentos_nombres) + f" {random.randint(10, 500)}mg"
        marca = random.choice(marcas) if random.choice([True, False]) else None
        precio = round(random.uniform(5.0, 150.0), 2)
        necesita_receta = random.choice([True, False])
        descripcion = fake.text(max_nb_chars=200) if random.choice([True, False]) else None
        
        medicamentos.append((nombre, marca, precio, necesita_receta, descripcion))
    
    try:
        # Insertar uno por uno para obtener los IDs
        medicamento_ids = []
        for medicamento in medicamentos:
            cur.execute("""
                INSERT INTO medicamento (nombre, marca, precio, necesita_receta, descripcion)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, medicamento)
            medicamento_ids.append(cur.fetchone()[0])
        
        conn.commit()
        print(f"✓ Insertados {num_medicamentos} medicamentos")
        return medicamento_ids
        
    except Exception as e:
        print(f"❌ Error insertando medicamentos: {e}")
        conn.rollback()
        return []
    finally:
        cur.close()
        conn.close()

def generate_clientes_empleados(user_dnis, sede_direcciones):
    """Genera clientes y empleados"""
    conn = connect_db()
    cur = conn.cursor()
    
    # 70% clientes, 30% empleados
    num_clientes = int(len(user_dnis) * 0.7)
    
    clientes_dnis = user_dnis[:num_clientes]
    empleados_dnis = user_dnis[num_clientes:]
    
    # Insertar clientes
    clientes = []
    for dni in clientes_dnis:
        direccion = f"Calle {fake.street_name()[:20]} {random.randint(100, 999)}"
        clientes.append((direccion, dni))
    
    try:
        cur.executemany("""
            INSERT INTO cliente (direccion, dni_usuario)
            VALUES (%s, %s)
        """, clientes)
        
        print(f"✓ Insertados {len(clientes)} clientes")
        
        # Insertar empleados
        empleados = []
        turnos = ["Mañana", "Tarde", "Noche", "Completo"]
        estados = ["Activo", "Inactivo", "Vacaciones"]
        
        for dni in empleados_dnis:
            direccion_sede = random.choice(sede_direcciones)
            sueldo = round(random.uniform(1000, 3000), 2)
            fecha_contratacion = fake.date_between(start_date='-3y', end_date='today')
            turno = random.choice(turnos)
            estado = random.choice(estados)
            
            empleados.append((dni, direccion_sede, sueldo, fecha_contratacion, turno, estado))
        
        cur.executemany("""
            INSERT INTO empleado (dni_usuario, direccion_sede, sueldo, fecha_contratacion, turno, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, empleados)
        
        conn.commit()
        print(f"✓ Insertados {len(empleados)} empleados")
        
        return clientes_dnis, empleados_dnis
        
    except Exception as e:
        print(f"❌ Error insertando clientes/empleados: {e}")
        conn.rollback()
        return [], []
    finally:
        cur.close()
        conn.close()

def generate_all_data():
    """Función principal para generar todos los datos"""
    print("🚀 Iniciando generación de datos fake...")
    
    # Limpiar tablas existentes
    clear_tables()
    
    # 1. Generar usuarios
    user_dnis = generate_users(100)
    if not user_dnis:
        return
    
    # 2. Generar sedes
    sede_direcciones = generate_sedes(10)
    if not sede_direcciones:
        return
    
    # 3. Generar medicamentos
    medicamento_ids = generate_medicamentos(50)
    if not medicamento_ids:
        return
    
    # 4. Generar clientes y empleados
    cliente_dnis, empleado_dnis = generate_clientes_empleados(user_dnis, sede_direcciones)
    if not cliente_dnis or not empleado_dnis:
        return
    
    print("✅ ¡Datos fake generados exitosamente!")
    print(f"📊 Resumen:")
    print(f"   - {len(user_dnis)} usuarios")
    print(f"   - {len(sede_direcciones)} sedes") 
    print(f"   - {len(medicamento_ids)} medicamentos")
    print(f"   - {len(cliente_dnis)} clientes")
    print(f"   - {len(empleado_dnis)} empleados")

if __name__ == "__main__":
    generate_all_data()