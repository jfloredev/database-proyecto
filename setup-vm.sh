#!/bin/bash
# Script de setup para VM EC2 - clonar desde Git y desplegar
# Ejecutar como: curl -fsSL https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/setup-vm.sh | bash

set -e

echo "🚀 Setup MiFarma en AWS EC2 desde Git"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variables - CONFIGURA ESTAS
REPO_URL="https://github.com/TU_USUARIO/TU_REPO.git"  # Cambiar por tu repo
BRANCH="main"
PUBLIC_IP=$(curl -s ifconfig.me)

echo -e "${YELLOW}IP pública detectada: ${PUBLIC_IP}${NC}"
echo ""

# 1. Instalar Docker si no existe
if ! command -v docker &> /dev/null; then
    echo "📦 Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}✓ Docker instalado${NC}"
else
    echo -e "${GREEN}✓ Docker ya instalado${NC}"
fi

# 2. Instalar Docker Compose si no existe
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose instalado${NC}"
else
    echo -e "${GREEN}✓ Docker Compose ya instalado${NC}"
fi

# 3. Instalar Git si no existe
if ! command -v git &> /dev/null; then
    echo "📦 Instalando Git..."
    sudo apt-get update
    sudo apt-get install -y git
    echo -e "${GREEN}✓ Git instalado${NC}"
else
    echo -e "${GREEN}✓ Git ya instalado${NC}"
fi

# 4. Clonar repositorio
PROJECT_DIR="$HOME/mifarma"
if [ -d "$PROJECT_DIR" ]; then
    echo "📂 Directorio existe, actualizando..."
    cd "$PROJECT_DIR"
    git pull origin "$BRANCH"
else
    echo "📂 Clonando repositorio..."
    git clone -b "$BRANCH" "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi
echo -e "${GREEN}✓ Código actualizado${NC}"

# 5. Crear archivo .env
echo "⚙️  Configurando variables de entorno..."
cat > .env << EOF
# Database
DB_HOST=postgres
DB_NAME=db_mifarma
DB_USER=postgres
DB_PASSWORD=$(openssl rand -base64 16)

# API URL - ajusta si tienes dominio
REACT_APP_API_BASE_URL=http://${PUBLIC_IP}:8080
EOF
echo -e "${GREEN}✓ Archivo .env creado${NC}"

# 6. Build y deploy
echo "🐳 Construyendo imágenes Docker..."
docker-compose build

echo "🚀 Levantando servicios..."
docker-compose up -d

echo "⏳ Esperando a PostgreSQL..."
sleep 30

echo "📊 Poblando base de datos..."
docker-compose exec -T backend python generate_sample_data.py || echo "⚠️  Datos ya existen o error al sembrar"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ ¡Despliegue completado!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "🌐 Accede a tu aplicación:"
echo "   Frontend: http://${PUBLIC_IP}:3004"
echo "   API Docs: http://${PUBLIC_IP}:8080/docs"
echo "   API Health: http://${PUBLIC_IP}:8080/health"
echo ""
echo "📊 Comandos útiles:"
echo "   Ver logs:      docker-compose logs -f"
echo "   Reiniciar:     docker-compose restart"
echo "   Detener:       docker-compose down"
echo "   Actualizar:    cd ~/mifarma && git pull && docker-compose up -d --build"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
echo "   - Asegúrate de que el Security Group permita puertos 8080 y 3004"
echo "   - Para cambiar la contraseña de DB, edita ~/mifarma/.env"
echo "   - Los datos persisten en el volumen 'pgdata'"
echo ""
