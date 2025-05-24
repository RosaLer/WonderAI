#!/bin/bash

# En caso de eror, salir
set -e

#Rutas para los Scripts de backend y fronted

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#Iniciando backend
echo "Iniciando backend en el puerto 8001..."
cd "$SCRIPT_DIR/src/backend"
uvicorn main:app --port 8001 --reload &

BACKEND_PID=$!

#Iniciando frontend
echo "Iniciando frontend (npm start)..."
cd "$SCRIPT_DIR/src/frontend"
npm start

#Al usar (Ctrl+C) se cierra todo
trap "echo 'Deteniendo backend (PID $BACKEND_PID)...'; kill $BACKEND_PID" EXIT
