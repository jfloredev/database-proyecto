# Arquitectura de MiFarma

## Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   Frontend (React)          │
        │   http://localhost:3004     │
        │                            │
        │  ┌──────────────────────┐  │
        │  │  SplashScreen        │  │
        │  │  (UTEC + Créditos)   │  │
        │  └──────────────────────┘  │
        │           ▼                 │
        │  ┌──────────────────────┐  │
        │  │   Header             │  │
        │  │  (MiFarma + Logo)    │  │
        │  └──────────────────────┘  │
        │           ▼                 │
        │  ┌──────────────────────┐  │
        │  │  NavTabs             │  │
        │  │ (5 Pestañas)         │  │
        │  └──────────────────────┘  │
        │           ▼                 │
        │  ┌──────────────────────┐  │
        │  │  Componentes Tabla   │  │
        │  │  - Usuarios          │  │
        │  │  - Clientes          │  │
        │  │  - Medicamentos      │  │
        │  │  - Empleados         │  │
        │  │  - Sedes             │  │
        │  └──────────────────────┘  │
        │           ▼                 │
        │  ┌──────────────────────┐  │
        │  │   Footer             │  │
        │  │  (Backend Info)      │  │
        │  └──────────────────────┘  │
        └────────────┬────────────────┘
                     │
                     │ HTTP/REST
                     │ API Calls
                     ▼
        ┌────────────────────────────┐
        │   Backend (FastAPI)         │
        │   http://localhost:8080     │
        │                            │
        │  ┌──────────────────────┐  │
        │  │  GET /usuarios       │  │
        │  │  GET /clientes       │  │
        │  │  GET /medicamentos   │  │
        │  │  GET /empleados      │  │
        │  │  GET /sedes          │  │
        │  │  + Más endpoints...  │  │
        │  └──────────────────────┘  │
        └────────────┬────────────────┘
                     │
                     │ SQL Queries
                     │ psycopg2
                     ▼
        ┌────────────────────────────┐
        │   PostgreSQL Database       │
        │   localhost:5432           │
        │   db_mifarma               │
        │                            │
        │  ┌──────────────────────┐  │
        │  │  Tablas:             │  │
        │  │  - usuario           │  │
        │  │  - cliente           │  │
        │  │  - medicamento       │  │
        │  │  - empleado          │  │
        │  │  - sede              │  │
        │  │  - inventario        │  │
        │  │  - venta             │  │
        │  │  - monedero          │  │
        │  │  + más...            │  │
        │  └──────────────────────┘  │
        └────────────────────────────┘
```

## Componentes Desacoplados

### 1. SplashScreen.tsx
- Portada inicial del sistema
- Logo UTEC profesional
- Título MiFarma con icono de salud
- Sección de créditos con integrantes
- Docente: Ing. Nina Wilder
- Botón "Ingresar al Sistema"
- Diseño con gradiente morado/azul

### 2. Header.tsx
- AppBar con logo MiFarma
- Ícono de medicina
- Subtítulo "Sistema de Gestión de Farmacia"
- Color consistente (#1976d2)

### 3. NavTabs.tsx
- 5 pestañas principales
- Iconos para cada sección
- Layout responsivo
- Navegación fácil entre módulos

### 4. Componentes de Tabla
Cada uno recibe props específicas:
- **UsuariosTable**: DNI, Nombre, Apellido, Teléfono, Email, Fecha Registro
- **ClientesTable**: ID, DNI, Nombre, Apellido, Dirección, Email
- **MedicamentosTable**: ID, Nombre, Marca, Precio, Requiere Receta
- **EmpleadosTable**: ID, Nombre, Sueldo, Turno, Estado, Sede
- **SedesTable**: Nombre, Dirección, Cantidad de Empleados

### 5. Footer.tsx
- Información del API Backend
- Puerto y dirección
- Ubicación consistente

## Flujo de Datos

1. Usuario abre la aplicación
2. Ve SplashScreen con portada profesional
3. Hace clic en "Ingresar al Sistema"
4. Se muestra la interfaz principal con Header + NavTabs
5. Al cambiar pestaña, se ejecuta fetch a API Backend
6. Backend consulta PostgreSQL
7. Los datos se renderizan en la tabla correspondiente
8. Todo con Material-UI para estilos profesionales

## Ventajas de la Arquitectura

✅ **Componentes Reutilizables**: Cada tabla es un componente independiente  
✅ **Separación de Responsabilidades**: Cada componente tiene una función clara  
✅ **Fácil Mantenimiento**: Cambios en un componente no afectan otros  
✅ **Escalabilidad**: Fácil agregar nuevas secciones  
✅ **TypeScript**: Tipado estricto previene errores  
✅ **Material-UI**: Estilos consistentes y profesionales  
✅ **Portada Personalizada**: Créditos del equipo y institución visible  

## Integrantes del Proyecto

**Estudiantes:**
- André Contreras
- André Ramos  
- Saúl Villanueva
- Renato Flores

**Docente:** Ing. Nina Wilder
**Universidad:** UTEC - Universidad de Ingeniería y Tecnología
