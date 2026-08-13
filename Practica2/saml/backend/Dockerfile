FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias nativas para python3-saml (xmlsec) y OpenSSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    pkg-config \
    openssl \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar paquetes de python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo
COPY . .

# Generar llaves y certificados auto-firmados para el SP
RUN mkdir -p certs && \
    openssl req -new -x509 -days 365 -nodes \
    -out certs/sp.crt \
    -keyout certs/sp.key \
    -subj "/C=ES/ST=Madrid/L=Madrid/O=SAML-POC/OU=Dev/CN=localhost"

# Puerto
EXPOSE 8001

# Levantar fastapi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
