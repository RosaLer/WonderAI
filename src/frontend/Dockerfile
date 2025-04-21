FROM node:18-slim

WORKDIR /app

# 1. Copiar solo los archivos necesarios para instalar dependencias
COPY package.json package-lock.json ./

# 2. Instalar dependencias con cache limpia
RUN npm ci --silent

# Verificación explícita de react-scripts (opcional)
RUN if [ ! -d "node_modules/react-scripts" ]; then npm install react-scripts; fi

# 3. Copiar el resto del código
COPY . .

# 4. Variables de entorno
ENV NODE_ENV=production \
    PORT=3000

# 5. Puerto expuesto
EXPOSE 3000

# 6. Comando de inicio
CMD ["npm", "start"]