# MiFarma - Sistema de Gestión de Farmacia

## 🚀 Despliegue Rápido en AWS desde Git

### Paso 1: Subir a GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/mifarma.git
git push -u origin main
```

### Paso 2: Configurar `setup-vm.sh`
Edita el archivo y cambia:
```bash
REPO_URL="https://github.com/TU_USUARIO/mifarma.git"
```

### Paso 3: Crear EC2 y ejecutar
```bash
# Crear EC2 Ubuntu 22.04, t2.medium
# Security Group: puertos 22, 8080, 3004

ssh -i tu-key.pem ubuntu@TU_IP
curl -fsSL https://raw.githubusercontent.com/TU_USUARIO/mifarma/main/setup-vm.sh | bash
```

### Paso 4: Acceder
- Frontend: `http://TU_IP:3004`
- API Docs: `http://TU_IP:8080/docs`

### Actualizar después de cambios
```bash
# Local
git add . && git commit -m "Update" && git push

# En EC2
cd ~/mifarma && git pull && docker-compose up -d --build
```

Ver [DEPLOY_AWS.md](./DEPLOY_AWS.md) para más opciones.

---

## 🐳 Desarrollo Local con Docker

```bash
cp .env.example .env
docker-compose up -d
docker-compose exec backend python generate_sample_data.py
# http://localhost:3004
```

---

## Estructura del Proyecto

### Frontend (React + TypeScript + Material-UI)

```
frontend/src/
├── App.tsx                    # Componente principal con lógica de ruteo
└── components/
    ├── index.ts               # Exportador centralizado de componentes
    ├── Header.tsx             # Barra superior con logo y título
    ├── Footer.tsx             # Pie de página con información
    ├── NavTabs.tsx            # Navegación por pestañas
    ├── SplashScreen.tsx       # Portada con logo UTEC, créditos e integrantes
    ├── UsuariosTable.tsx      # Tabla de usuarios
    ├── ClientesTable.tsx      # Tabla de clientes
    ├── MedicamentosTable.tsx  # Tabla de medicamentos
    ├── EmpleadosTable.tsx     # Tabla de empleados
    └── SedesTable.tsx         # Tabla de sedes
```

### Backend (FastAPI + Python)

```
backend/
├── main.py                    # API FastAPI con 20+ endpoints
├── config.py                  # Configuración de la aplicación
├── database.py                # Configuración de conexión a BD
├── generate_sample_data.py    # Script para generar datos de prueba
├── requirements.txt           # Dependencias de Python
├── .env                       # Variables de entorno
└── .gitignore                 # Archivos ignorados
```

## Credenciales del Proyecto

**Equipo de Desarrollo:**
- André Contreras
- André Ramos
- Saúl Villanueva
- Renato Flores

**Docente:** Ing. Nina Wilder

**Institución:** UTEC - Universidad de Ingeniería y Tecnología

## Características

### Frontend
✅ Desacoplamiento de componentes para mejor mantenibilidad  
✅ Portada profesional con logo UTEC  
✅ Navegación por pestañas  
✅ Tablas dinámicas con Material-UI  
✅ Tipado completo con TypeScript  
✅ Estilos consistentes con Material-UI

### Backend
✅ API REST con FastAPI  
✅ 20+ endpoints para consultas  
✅ Conexión a PostgreSQL  
✅ CORS habilitado para frontend  
✅ Generación de datos de prueba  
✅ Gestión de usuarios, clientes, medicamentos, empleados y sedes

## Puertos

- **Frontend:** http://localhost:3004
- **Backend:** http://localhost:8080

## Iniciar el Proyecto

### Frontend
```bash
cd frontend
npm install
npm start
```

### Backend
```bash
cd backend
source .venv/bin/activate
python -m uvicorn main:app --reload --port 8080
```

## Base de Datos

**PostgreSQL**
- Base de datos: `db_mifarma`
- Usuario: `postgres`
- Contraseña: `12345678`
- Host: `localhost`
- Puerto: `5432`

### Tablas Principales
- usuario
- cliente
- medicamento
- empleado
- sede
- inventario
- venta
- monedero
- receta_medica
- detalles_venta
- reserva
- delivery
- promocion
