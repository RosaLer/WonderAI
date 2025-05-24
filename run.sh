#!/bin/bash

# Salir si ocurre algún error
set -e

# Ruta absoluta al script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Iniciar backend (puerto 8001 con recarga automática)
echo "🚀 Iniciando backend en el puerto 8001..."
cd "$SCRIPT_DIR/src/backend"
uvicorn main:app --port 8001 --reload &

# Guardar el PID del backend para poder matarlo al final
BACKEND_PID=$!

# Iniciar frontend
echo "🌐 Iniciando frontend (npm start)..."
cd "$SCRIPT_DIR/src/frontend"
npm start

# Si cierras el frontend (Ctrl+C), también se cierra el backend
trap "echo '🛑 Deteniendo backend (PID $BACKEND_PID)...'; kill $BACKEND_PID" EXIT
