# SAML 2.0 Backend (Service Provider)

Este es el servicio backend de la **Proof of Concept (POC) de SAML 2.0**. Está construido con FastAPI (Python) y actúa como un **Service Provider (SP)** que delega la autenticación a Keycloak, operando como **Identity Provider (IdP)**.

## 1. Objetivo
Demostrar el funcionamiento de SAML 2.0 en un escenario de federación e inicio de sesión único (SSO). El backend genera solicitudes de autenticación firmadas, valida y descifra respuestas SAML del IdP, lee las Assertiones SAML y expone recursos protegidos basándose en la sesión SAML establecida.

## 2. Tecnologías
* **Python 3.12+**
* **FastAPI**
* **python3-saml** (Librería de OneLogin para SAML 2.0 SP)
* **xmlsec** (Herramienta criptográfica para la firma/validación XML)
* **OpenSSL** (Generación de claves SP en Docker build)

## 3. Metadata
El backend expone un endpoint autogenerado de metadatos en:
* `GET /saml/metadata`

Este XML expone la configuración del Service Provider (Entity ID, ACS URL, llaves criptográficas públicas) para importación automática en Keycloak.

## 4. Endpoints
* `GET /health`: Estado del servicio.
* `GET /login`: Genera una `AuthnRequest` de SAML y redirige al navegador a Keycloak.
* `POST /saml/acs`: Endpoint del Assertion Consumer Service. Recibe y procesa el POST enviado por Keycloak con la respuesta SAML encriptada/firmada. Establece una cookie firmada local.
* `GET /saml/metadata`: Genera el XML de metadatos del SP.
* `GET /api/profile`: Endpoint protegido que retorna claims de la Assertion (NameID, email, nombre, emisor, condiciones).
* `GET /logout`: Elimina cookies locales y redirige a la URL de cierre de sesión de Keycloak.

## 5. Seguridad
* **Certificados Criptográficos**: Genera un par de llaves auto-firmadas al compilar la imagen de Docker para firmar llamadas de autenticación y verificar el cifrado.
* **Firmas de Assertions**: Valida la firma digital de Keycloak sobre la Assertion XML para asegurar que no ha sido alterada.
* **Protección Anti-Replay**: El módulo valida timestamps, vigencia temporal de las Assertions (`NotBefore` y `NotOnOrAfter`) e ID del emisor.
* **Cookies de Sesión Firmadas**: Emplea firmas criptográficas con clave secreta (`itsdangerous`) en cookies HttpOnly para el control de sesiones.

## 6. Ejecución local (sin Docker)
1. Instalar dependencias nativas del sistema (requerido para `xmlsec`):
   * Ubuntu/Debian:
     ```bash
     sudo apt-get install -y libxml2-dev libxslt1-dev libxmlsec1-dev libxmlsec1-openssl build-essential pkg-config
     ```
2. Instalar dependencias python:
   ```bash
   pip install -r requirements.txt
   ```
3. Generar certificados locales en una carpeta `certs/` paralela a `app/`:
   ```bash
   mkdir certs
   openssl req -new -x509 -days 365 -nodes -out certs/sp.crt -keyout certs/sp.key -subj "/CN=localhost"
   ```
4. Ejecutar:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```
