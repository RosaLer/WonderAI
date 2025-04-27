FROM node:12.22.12-stretch-slim  

WORKDIR /app

# 1. Copiar solo los archivos necesarios para instalar dependencias
COPY package.json ./
RUN npm install --silent --no-optional && \
    npm cache clean --force

# 2. Copiar el resto (ahora incluyendo package-lock.json generado)
COPY . .

# 3. Configuración para macOS antiguo
ENV CI=true
ENV NODE_OPTIONS="--max-old-space-size=2048"

EXPOSE 3000
CMD ["npm", "start"]