# OAuth 2.0 + OIDC Backend

Este es el servicio backend de la **Proof of Concept (POC) de OAuth 2.0 y OpenID Connect (OIDC)**. Está construido con FastAPI (Python) y se integra con Keycloak como Identity Provider (IdP) utilizando el flujo **Authorization Code Flow**.

## 1. Objetivo
Demostrar el flujo de autorización y la delegación de identidad. El backend actúa como un cliente web confidencial (Confidential Client), interactúa con Keycloak para intercambiar códigos de autorización por tokens, valida los tokens mediante JWKS y expone endpoints protegidos.

## 2. Tecnologías
* **Python 3.12+**
* **FastAPI**
* **Uvicorn** (Servidor ASGI)
* **Python-jose** (Validación de tokens JWT)
* **Requests** (Comunicación HTTP síncrona con Keycloak)

## 3. Endpoints
El backend expone los siguientes endpoints:
* `GET /health`: Estado del servicio.
* `GET /login`: Redirige al navegador a Keycloak para autenticar al usuario.
* `GET /callback`: Recibe el código de autorización de Keycloak, lo intercambia por tokens, valida el ID Token, establece cookies HttpOnly de sesión y redirige al frontend.
* `GET /api/profile`: Endpoint protegido. Verifica la sesión y retorna la identidad del usuario (claims) y la disponibilidad del Access Token.
* `GET /logout`: Cierra sesión localmente (borra cookies) y redirige a Keycloak para Single Logout (SLO).

## 4. Seguridad
* **HttpOnly Session Cookies**: Evita que los tokens sean accesibles desde JavaScript en el navegador, mitigando ataques XSS.
* **Keycloak Token Validation**: Valida las firmas de los tokens JWT usando el JWKS endpoint público de Keycloak.
* **Separación de Hosts**: Usa `KEYCLOAK_URL` (para el navegador del cliente) y `KEYCLOAK_URL_INTERNAL` (para llamadas directas contenedor a contenedor), resolviendo conflictos de red en Docker.
* **Confidential Client**: El Client Secret se maneja de forma segura mediante variables de entorno y no se expone al cliente.

## 5. Cómo ejecutar localmente (sin Docker)
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Iniciar el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
