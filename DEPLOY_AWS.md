# Despliegue en AWS con Docker Compose

Guía rápida para desplegar MiFarma en una instancia EC2 con datos persistentes.

## 🚀 Método 1: Despliegue desde Git (Recomendado)

### Requisitos previos
- Cuenta AWS con acceso a EC2
- Par de claves SSH (.pem)
- Repositorio Git con el código (GitHub/GitLab/Bitbucket)

### Paso 1: Subir código a Git

```bash
# En tu Mac
cd /Users/juanrenato/UTEC/tercerCiclo/DataBase/app-Mifarma

# Inicializar Git si no lo has hecho
git init
git add .
git commit -m "Initial commit: MiFarma app"

# Crear repo en GitHub y subir
git remote add origin https://github.com/TU_USUARIO/mifarma.git
git branch -M main
git push -u origin main
```

### Paso 2: Crear instancia EC2

1. **Lanzar instancia**:
   - AMI: Ubuntu Server 22.04 LTS
   - Tipo: `t2.medium` o superior (mínimo 2 GB RAM)
   - Storage: 20 GB gp3
   - Security Group:
     - SSH (22) desde tu IP
     - HTTP (80) desde 0.0.0.0/0
     - Custom TCP (8080) desde 0.0.0.0/0
     - Custom TCP (3004) desde 0.0.0.0/0

2. **Anotar IP pública**: Ejemplo `54.123.45.67`

### Paso 3: Configurar script de setup

Antes de ejecutar, edita `setup-vm.sh` en tu repo y cambia:
```bash
REPO_URL="https://github.com/TU_USUARIO/mifarma.git"  # Tu URL de Git
```

Haz commit y push del cambio.

### Paso 4: Ejecutar setup automático

```bash
# SSH a la instancia
ssh -i ~/.ssh/tu-key.pem ubuntu@54.123.45.67

# Opción A: Ejecutar script directo desde GitHub (más rápido)
curl -fsSL https://raw.githubusercontent.com/TU_USUARIO/mifarma/main/setup-vm.sh | bash

# Opción B: Clonar primero y ejecutar local
git clone https://github.com/TU_USUARIO/mifarma.git
cd mifarma
chmod +x setup-vm.sh
./setup-vm.sh
```

El script automáticamente:
- ✅ Instala Docker y Docker Compose
- ✅ Clona el repositorio
- ✅ Crea archivo `.env` con contraseña segura
- ✅ Build de imágenes
- ✅ Levanta servicios
- ✅ Siembra datos de ejemplo

### Paso 5: Actualizar la aplicación

```bash
# Para actualizar después de hacer cambios
cd ~/mifarma
git pull
docker-compose up -d --build
```

---

## 📦 Método 2: Despliegue manual (transferencia SCP)

### Requisitos previos
- Cuenta AWS con acceso a EC2
- Par de claves SSH (.pem)
- Docker Desktop instalado localmente (para build opcional)

## Paso 1: Crear instancia EC2

1. **Lanzar instancia**:
   - AMI: Ubuntu Server 22.04 LTS
   - Tipo: `t2.medium` o superior (mínimo 2 GB RAM)
   - Storage: 20 GB gp3
   - Security Group:
     - SSH (22) desde tu IP
     - HTTP (80) desde 0.0.0.0/0
     - Custom TCP (8080) desde 0.0.0.0/0
     - Custom TCP (3004) desde 0.0.0.0/0
     - PostgreSQL (5432) SOLO desde el security group mismo (opcional para debug)

2. **Anotar IP pública**: Ejemplo `54.123.45.67`

## Paso 1: Crear instancia EC2

```bash
# SSH a la instancia (reemplaza tu-key.pem e IP)
ssh -i ~/.ssh/tu-key.pem ubuntu@54.123.45.67

# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
rm get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar
docker --version
docker-compose --version

# Reiniciar sesión para aplicar grupo docker
exit
```

## Paso 2: Conectar y configurar servidor

```bash
# Desde tu Mac (en el directorio del proyecto)
cd /Users/juanrenato/UTEC/tercerCiclo/DataBase/app-Mifarma

# Comprimir proyecto (excluir archivos innecesarios)
tar -czf mifarma.tar.gz \
  --exclude='.venv' \
  --exclude='node_modules' \
  --exclude='frontend/build' \
  --exclude='__pycache__' \
  --exclude='.git' \
  backend/ frontend/ docker-compose.yml .dockerignore

# Copiar a EC2 (reemplaza tu-key.pem e IP)
scp -i ~/.ssh/tu-key.pem mifarma.tar.gz ubuntu@54.123.45.67:~/

# SSH nuevamente
ssh -i ~/.ssh/tu-key.pem ubuntu@54.123.45.67

# Descomprimir
tar -xzf mifarma.tar.gz
cd ~/
```

## Paso 3: Subir proyecto a EC2

```bash
# Crear archivo .env en el servidor
cat > .env << 'EOF'
# Database
DB_HOST=postgres
DB_NAME=db_mifarma
DB_USER=postgres
DB_PASSWORD=SecurePasswordHere123

# API URL para frontend (reemplaza con tu IP pública o dominio)
REACT_APP_API_BASE_URL=http://54.123.45.67:8080
EOF
```

## Paso 4: Configurar variables de entorno

Crea o edita `docker-compose.yml` en el servidor con persistencia:

```yaml
version: '3.9'
services:
  postgres:
    image: postgres:15
    container_name: mifarma_postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: mifarma_backend
    environment:
      DB_HOST: ${DB_HOST}
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8080:8080"
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        REACT_APP_API_BASE_URL: ${REACT_APP_API_BASE_URL}
    container_name: mifarma_frontend
    depends_on:
      - backend
    ports:
      - "3004:80"
    restart: unless-stopped

volumes:
  pgdata:
    driver: local
```

## Paso 5: Desplegar aplicación

```bash
# Build imágenes (tarda 5-10 min la primera vez)
docker-compose build

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Verificar estado
docker-compose ps
```

## Paso 6: Inicializar base de datos con datos de ejemplo

```bash
# Esperar 30 segundos a que Postgres arranque completamente
sleep 30

# Ejecutar script de seed dentro del contenedor backend
docker-compose exec backend python generate_sample_data.py
```

## Paso 7: Acceder a la aplicación

- **Frontend**: http://54.123.45.67:3004 (reemplaza con tu IP)
- **API**: http://54.123.45.67:8080/health
- **API Docs**: http://54.123.45.67:8080/docs

## Persistencia de datos

Los datos de PostgreSQL se almacenan en un **volumen Docker nombrado** (`pgdata`), que persiste incluso si:
- Detienes los contenedores: `docker-compose down`
- Actualizas el código y reconstruyes: `docker-compose up -d --build`
- Reinicias la instancia EC2

**Para hacer backup manual**:
```bash
# Backup
docker-compose exec postgres pg_dump -U postgres db_mifarma > backup_$(date +%Y%m%d).sql

# Restaurar
cat backup_20251128.sql | docker-compose exec -T postgres psql -U postgres db_mifarma
```

## Comandos útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Reiniciar un servicio
docker-compose restart backend

# Actualizar código y reconstruir
docker-compose down
docker-compose build
docker-compose up -d

# Conectar a Postgres directamente
docker-compose exec postgres psql -U postgres -d db_mifarma

# Limpiar todo (CUIDADO: borra los datos)
docker-compose down -v
```

## Opcional: Configurar dominio y HTTPS

Si tienes un dominio (ej. `mifarma.tudominio.com`):

1. **Apuntar dominio a la IP de EC2** (A record en tu DNS)

2. **Instalar Nginx como reverse proxy con SSL**:
```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Configurar Nginx para proxy
sudo nano /etc/nginx/sites-available/mifarma

# Agregar configuración:
server {
    listen 80;
    server_name mifarma.tudominio.com;

    location / {
        proxy_pass http://localhost:3004;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Activar sitio
sudo ln -s /etc/nginx/sites-available/mifarma /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Obtener certificado SSL (gratis con Let's Encrypt)
sudo certbot --nginx -d mifarma.tudominio.com
```

3. **Actualizar `REACT_APP_API_BASE_URL`** en `.env`:
```bash
REACT_APP_API_BASE_URL=https://mifarma.tudominio.com/api
```

4. **Reconstruir frontend**:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

## Monitoreo y mantenimiento

- **Logs de sistema**: `sudo journalctl -u docker -f`
- **Uso de recursos**: `docker stats`
- **Espacio en disco**: `df -h` y `docker system df`
- **Actualizar imágenes base**: `docker-compose pull && docker-compose up -d`

## Costos estimados AWS (región us-east-1)

- **EC2 t2.medium**: ~$30/mes (On-Demand) o ~$7/mes (Spot)
- **EBS 20 GB**: ~$2/mes
- **Transferencia**: Primeros 100 GB/mes gratis, luego $0.09/GB
- **IP elástica**: Gratis si está asignada a instancia corriendo

**Total estimado**: $10-35/mes dependiendo de tráfico y uso de Spot instances.

## Troubleshooting

**Frontend no carga**:
```bash
# Verificar que REACT_APP_API_BASE_URL esté correcto
docker-compose logs frontend | grep REACT_APP
# Reconstruir si es necesario
docker-compose build frontend --no-cache
```

**Backend no conecta a DB**:
```bash
# Verificar variables de entorno
docker-compose exec backend env | grep DB_
# Ver logs de Postgres
docker-compose logs postgres
```

**Puerto en uso**:
```bash
# Ver qué usa el puerto
sudo lsof -i :8080
# Detener servicios conflictivos
sudo systemctl stop <servicio>
```

**Sin espacio en disco**:
```bash
# Limpiar contenedores viejos
docker system prune -a
# Limpiar volúmenes no usados (CUIDADO)
docker volume prune
```
