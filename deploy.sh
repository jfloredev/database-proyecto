#!/bin/bash
# Script de despliegue rápido en EC2
# Ejecutar en el servidor después de subir archivos

set -e

echo "🚀 Desplegando MiFarma en AWS EC2..."

# 1. Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no instalado. Instalar primero."
    exit 1
fi

# 2. Crear .env si no existe
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env..."
    cat > .env << 'EOF'
DB_HOST=postgres
DB_NAME=db_mifarma
DB_USER=postgres
DB_PASSWORD=ChangeThisPassword123

# Reemplaza con tu IP pública o dominio
REACT_APP_API_BASE_URL=http://YOUR_PUBLIC_IP:8080
EOF
    echo "⚠️  IMPORTANTE: Edita .env y actualiza REACT_APP_API_BASE_URL con tu IP pública"
    echo "   Ejecuta: nano .env"
    exit 0
fi

# 3. Build y deploy
echo "📦 Construyendo imágenes (esto tarda unos minutos)..."
docker-compose build

echo "🐳 Levantando servicios..."
docker-compose up -d

echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 30

echo "📊 Poblando base de datos con datos de ejemplo..."
docker-compose exec -T backend python generate_sample_data.py || echo "⚠️  Error al sembrar datos (puede ser normal si ya existen)"

echo ""
echo "✅ ¡Despliegue completado!"
echo ""
echo "🌐 Accede a tu aplicación:"
echo "   Frontend: http://$(curl -s ifconfig.me):3004"
echo "   API: http://$(curl -s ifconfig.me):8080/docs"
echo ""
echo "📊 Ver logs: docker-compose logs -f"
echo "🔄 Reiniciar: docker-compose restart"
echo "🛑 Detener: docker-compose down"
echo ""
