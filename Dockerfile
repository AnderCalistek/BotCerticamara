# Usar la imagen oficial ligera de Python
FROM python:3.11-slim

# Evitar  y forzar salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



ENV IN_DOCKER=true

# Crear las carpetas que el bot espera encontrar
RUN mkdir -p /app/input /app/output/SIGA_GESTION

# Instalar dependencias del sistema requeridas para ejecutar Chrome Headless en Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    libdbus-1-3 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    libasound2t64 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Google Chrome usando el método moderno (sin apt-key obsoleto)
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias optimizado e instalarlas
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copiar todo el código de scripts de automatización del backend al contenedor
COPY . .

# Comando por defecto para mantener el contenedor interactivo o ejecutar pruebas
CMD ["python", "PROCESO_COMPLETO.py"]
