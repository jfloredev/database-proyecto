from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_settings
import os

settings = get_settings()

app = FastAPI(
    title="MiFarma API",
    description="API para gestión de farmacia",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Obtiene conexión a la base de datos (configurable por variables de entorno)."""
    host = os.getenv("DB_HOST", "localhost")
    database = os.getenv("DB_NAME", "db_mifarma")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "12345678")
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        cursor_factory=RealDictCursor
    )

@app.get("/")
async def root():
    return {"message": "Bienvenido a MiFarma API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/usuarios")
async def get_usuarios():
    """Obtiene todos los usuarios"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM usuario ORDER BY nombre")
        usuarios = cur.fetchall()
        return {"usuarios": usuarios, "total": len(usuarios)}
    finally:
        cur.close()
        conn.close()

@app.get("/clientes")
async def get_clientes():
    """Obtiene todos los clientes con información de usuario"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT c.id, c.direccion, u.dni, u.nombre, u.apellido, u.telefono, u.email
            FROM cliente c
            JOIN usuario u ON c.dni_usuario = u.dni
            ORDER BY u.nombre
        """)
        clientes = cur.fetchall()
        return {"clientes": clientes, "total": len(clientes)}
    finally:
        cur.close()
        conn.close()

@app.get("/medicamentos")
async def get_medicamentos():
    """Obtiene todos los medicamentos"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM medicamento ORDER BY nombre")
        medicamentos = cur.fetchall()
        return {"medicamentos": medicamentos, "total": len(medicamentos)}
    finally:
        cur.close()
        conn.close()

@app.get("/empleados")
async def get_empleados():
    """Obtiene todos los empleados con información de usuario y sede"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT e.id, u.dni, u.nombre, u.apellido, e.sueldo, e.turno, e.estado,
                   s.nombre as sede_nombre, e.direccion_sede
            FROM empleado e
            JOIN usuario u ON e.dni_usuario = u.dni
            JOIN sede s ON e.direccion_sede = s.direccion
            ORDER BY u.nombre
        """)
        empleados = cur.fetchall()
        return {"empleados": empleados, "total": len(empleados)}
    finally:
        cur.close()
        conn.close()

@app.get("/sedes")
async def get_sedes():
    """Obtiene todas las sedes"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM sede ORDER BY nombre")
        sedes = cur.fetchall()
        return {"sedes": sedes, "total": len(sedes)}
    finally:
        cur.close()
        conn.close()

@app.get("/medicamentos/{medicamento_id}")
async def get_medicamento(medicamento_id: int):
    """Obtiene un medicamento específico"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM medicamento WHERE id = %s", (medicamento_id,))
        medicamento = cur.fetchone()
        
        if not medicamento:
            return {"error": "Medicamento no encontrado"}
        
        return {"medicamento": medicamento}
    finally:
        cur.close()
        conn.close()

@app.get("/clientes/{cliente_id}")
async def get_cliente(cliente_id: int):
    """Obtiene un cliente específico con su información"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT c.id, c.direccion, u.dni, u.nombre, u.apellido, u.telefono, u.email, u.fecha_registro
            FROM cliente c
            JOIN usuario u ON c.dni_usuario = u.dni
            WHERE c.id = %s
        """, (cliente_id,))
        cliente = cur.fetchone()
        
        if not cliente:
            return {"error": "Cliente no encontrado"}
        
        return {"cliente": cliente}
    finally:
        cur.close()
        conn.close()

# ==================== ENDPOINTS DE LÓGICA DE NEGOCIO ====================

@app.get("/medicamentos/search/{nombre}")
async def search_medicamentos(nombre: str):
    """Busca medicamentos por nombre (para el frontend de búsqueda)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM medicamento 
            WHERE nombre ILIKE %s 
            ORDER BY nombre
        """, (f"%{nombre}%",))
        medicamentos = cur.fetchall()
        return {"medicamentos": medicamentos, "total": len(medicamentos)}
    finally:
        cur.close()
        conn.close()

@app.get("/medicamentos/receta/{necesita_receta}")
async def get_medicamentos_by_receta(necesita_receta: bool):
    """Obtiene medicamentos según si necesitan receta o no"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM medicamento 
            WHERE necesita_receta = %s 
            ORDER BY precio
        """, (necesita_receta,))
        medicamentos = cur.fetchall()
        tipo = "con receta" if necesita_receta else "sin receta"
        return {
            "medicamentos": medicamentos, 
            "total": len(medicamentos),
            "tipo": tipo
        }
    finally:
        cur.close()
        conn.close()

@app.get("/medicamentos/precio-rango")
async def get_medicamentos_por_precio(precio_min: float = 0, precio_max: float = 1000):
    """Obtiene medicamentos en un rango de precios"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT *, precio::float as precio_num FROM medicamento 
            WHERE precio BETWEEN %s AND %s 
            ORDER BY precio
        """, (precio_min, precio_max))
        medicamentos = cur.fetchall()
        return {
            "medicamentos": medicamentos, 
            "total": len(medicamentos),
            "rango": f"S/{precio_min} - S/{precio_max}"
        }
    finally:
        cur.close()
        conn.close()

@app.get("/empleados/sede/{sede_nombre}")
async def get_empleados_por_sede(sede_nombre: str):
    """Obtiene empleados de una sede específica"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT e.id, u.dni, u.nombre, u.apellido, e.sueldo, e.turno, e.estado,
                   s.nombre as sede_nombre
            FROM empleado e
            JOIN usuario u ON e.dni_usuario = u.dni
            JOIN sede s ON e.direccion_sede = s.direccion
            WHERE s.nombre ILIKE %s
            ORDER BY u.nombre
        """, (f"%{sede_nombre}%",))
        empleados = cur.fetchall()
        return {"empleados": empleados, "total": len(empleados), "sede": sede_nombre}
    finally:
        cur.close()
        conn.close()

@app.get("/empleados/turno/{turno}")
async def get_empleados_por_turno(turno: str):
    """Obtiene empleados por turno de trabajo"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT e.id, u.dni, u.nombre, u.apellido, e.turno, e.estado,
                   s.nombre as sede_nombre
            FROM empleado e
            JOIN usuario u ON e.dni_usuario = u.dni
            JOIN sede s ON e.direccion_sede = s.direccion
            WHERE e.turno = %s AND e.estado = 'Activo'
            ORDER BY u.nombre
        """, (turno,))
        empleados = cur.fetchall()
        return {"empleados": empleados, "total": len(empleados), "turno": turno}
    finally:
        cur.close()
        conn.close()

@app.get("/clientes/buscar/{criterio}")
async def search_clientes(criterio: str):
    """Busca clientes por nombre, apellido o DNI"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT c.id, c.direccion, u.dni, u.nombre, u.apellido, u.telefono, u.email
            FROM cliente c
            JOIN usuario u ON c.dni_usuario = u.dni
            WHERE u.nombre ILIKE %s OR u.apellido ILIKE %s OR u.dni LIKE %s
            ORDER BY u.nombre
        """, (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"))
        clientes = cur.fetchall()
        return {"clientes": clientes, "total": len(clientes), "criterio": criterio}
    finally:
        cur.close()
        conn.close()

@app.get("/estadisticas/resumen")
async def get_estadisticas_resumen():
    """Obtiene estadísticas generales del sistema"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        estadisticas = {}
        
        # Total usuarios
        cur.execute("SELECT COUNT(*) FROM usuario")
        estadisticas["total_usuarios"] = cur.fetchone()["count"]
        
        # Total clientes
        cur.execute("SELECT COUNT(*) FROM cliente")
        estadisticas["total_clientes"] = cur.fetchone()["count"]
        
        # Total empleados activos
        cur.execute("SELECT COUNT(*) FROM empleado WHERE estado = 'Activo'")
        estadisticas["empleados_activos"] = cur.fetchone()["count"]
        
        # Total medicamentos
        cur.execute("SELECT COUNT(*) FROM medicamento")
        estadisticas["total_medicamentos"] = cur.fetchone()["count"]
        
        # Medicamentos que necesitan receta
        cur.execute("SELECT COUNT(*) FROM medicamento WHERE necesita_receta = true")
        estadisticas["medicamentos_con_receta"] = cur.fetchone()["count"]
        
        # Total sedes
        cur.execute("SELECT COUNT(*) FROM sede")
        estadisticas["total_sedes"] = cur.fetchone()["count"]
        
        # Precio promedio medicamentos
        cur.execute("SELECT AVG(precio)::float as promedio FROM medicamento")
        estadisticas["precio_promedio_medicamentos"] = round(cur.fetchone()["promedio"], 2)
        
        return {"estadisticas": estadisticas}
    finally:
        cur.close()
        conn.close()

@app.get("/sedes/{sede_direccion}/empleados")
async def get_empleados_de_sede(sede_direccion: str):
    """Obtiene todos los empleados de una sede específica"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT e.id, u.dni, u.nombre, u.apellido, e.sueldo, e.turno, e.estado,
                   e.fecha_contratacion, s.nombre as sede_nombre
            FROM empleado e
            JOIN usuario u ON e.dni_usuario = u.dni
            JOIN sede s ON e.direccion_sede = s.direccion
            WHERE s.direccion = %s
            ORDER BY u.nombre
        """, (sede_direccion,))
        empleados = cur.fetchall()
        
        # También obtener info de la sede
        cur.execute("SELECT * FROM sede WHERE direccion = %s", (sede_direccion,))
        sede = cur.fetchone()
        
        return {
            "sede": sede,
            "empleados": empleados, 
            "total_empleados": len(empleados)
        }
    finally:
        cur.close()
        conn.close()

@app.get("/usuarios/recientes")
async def get_usuarios_recientes(dias: int = 30):
    """Obtiene usuarios registrados en los últimos N días"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM usuario 
            WHERE fecha_registro >= CURRENT_DATE - INTERVAL '%s days'
            ORDER BY fecha_registro DESC
        """, (dias,))
        usuarios = cur.fetchall()
        return {
            "usuarios_recientes": usuarios, 
            "total": len(usuarios),
            "periodo": f"Últimos {dias} días"
        }
    finally:
        cur.close()
        conn.close()

@app.get("/monedero")
async def get_monedero():
    """Obtiene el saldo de monedero de todos los clientes"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT m.id, m.saldo, m.fecha_creacion, m.dni_cliente
            FROM monedero m
            ORDER BY m.id
        """)
        monederos = cur.fetchall()
        return {"monedero": monederos, "total": len(monederos)}
    finally:
        cur.close()
        conn.close()

