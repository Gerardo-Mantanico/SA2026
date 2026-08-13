# OAuth 2.0 + OIDC vs SAML 2.0 - Proof of Concept (POC)

Este proyecto académico implementa y compara de forma práctica dos de los mecanismos de delegación de identidad y Single Sign-On (SSO) más utilizados en la industria:
1. **OAuth 2.0 + OpenID Connect (OIDC)**
2. **SAML 2.0**

El objetivo principal es demostrar sus flujos de autenticación, diferencias de arquitectura, ventajas, complejidades y casos de uso prácticos.

---

## 1. Arquitectura General

El proyecto consta de 5 servicios dockerizados:
* **Keycloak (Identity Provider - IdP)**: Centraliza las identidades en el puerto `8080`. Contiene dos Realms independientes auto-configurados al arrancar: `oauth-realm` y `saml-realm`.
* **OIDC POC (Puerto 3000 / 8000)**:
  * **Backend (FastAPI)**: Servidor cliente que procesa el código de autorización y valida tokens OIDC.
  * **Frontend (React)**: Interfaz de usuario moderna para iniciar sesión, consultar claims de ID Token y comprobar disponibilidad de Access Token.
* **SAML POC (Puerto 3001 / 8001)**:
  * **Backend (FastAPI)**: Service Provider (SP) que procesa Assertiones SAML firmadas. Genera metadatos XML públicos y auto-genera llaves criptográficas de confianza al compilar.
  * **Frontend (React)**: Interfaz que visualiza los detalles de la SAML Assertion (Subject NameID, Issuer, Conditions, etc.).

```text
                         ┌─────────────────────┐
                         │      Keycloak       │
                         │   Identity Provider │
                         │   (Port 8080)       │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
              OAuth 2.0 + OIDC                 SAML 2.0
                    │                               │
                    ▼                               ▼
          ┌───────────────────┐           ┌───────────────────┐
          │    OAuth POC      │           │     SAML POC      │
          │                   │           │                   │
          │ React + FastAPI   │           │ React + FastAPI   │
          │ Ports: 3000/8000  │           │ Ports: 3001/8001  │
          └───────────────────┘           └───────────────────┘
```

---

## 2. Estructura de Carpetas

```text
oauth-vs-saml-poc/
├── README.md                 <- Este archivo (Instrucciones generales)
├── docker-compose.yml        <- Orquestador de contenedores
├── .gitignore
├── .env.example              <- Variables de entorno plantilla
├── .env                      <- Variables de entorno configuradas
│
├── keycloak/
│   └── imports/              <- Realms preconfigurados para OIDC y SAML
│       ├── oauth-realm.json
│       └── saml-realm.json
│
├── oauth-oidc/
│   ├── backend/              <- API FastAPI para OIDC
│   └── frontend/             <- App React (Vite) para OIDC
│
├── saml/
│   ├── backend/              <- API FastAPI + python3-saml (SP)
│   └── frontend/             <- App React (Vite) para SAML
│
└── docs/
    ├── oauth-flow.md         <- Documentación del flujo OIDC con diagramas
    ├── saml-flow.md          <- Documentación del flujo SAML con diagramas
    └── comparison.md         <- Tabla comparativa y análisis detallado
```

---

## 3. Requisitos Previos

Asegúrate de tener instalados en tu sistema:
* **Docker** (v20+)
* **Docker Compose** (v2+)

---

## 4. Instrucciones para Ejecutar el Proyecto

1. **Clonar el repositorio** y posicionarse en la carpeta raíz.
2. **Crear archivo de variables de entorno**:
   Copiar la plantilla `.env.example` para generar el archivo `.env`:
   ```bash
   cp .env.example .env
   ```
3. **Iniciar los servicios**:
   Ejecuta el siguiente comando para compilar e iniciar todos los servicios:
   ```bash
   docker compose up --build
   ```
   *Nota: Keycloak puede tardar unos segundos en arrancar por primera vez e importar los realms configurados. Los backends esperarán a que Keycloak esté saludable para activarse.*

---

## 5. Instrucciones de Prueba y Credenciales

### 5.1 Identity Provider (Keycloak)
* **Consola de Administración**: [http://localhost:8080](http://localhost:8080)
* **Credenciales de Admin**: `admin` / `admin`

### 5.2 POC 1: OAuth 2.0 + OpenID Connect
1. Accede al frontend OIDC en [http://localhost:3000](http://localhost:3000).
2. Haz clic en **"Iniciar sesión con Keycloak"**.
3. Redirigirá a Keycloak. Inicia sesión con:
   * **Usuario**: `oauth-user`
   * **Contraseña**: `password`
4. Tras autenticarte, serás redirigido de vuelta al frontend. Podrás ver tus claims (nombre, email, username) y el estado `Access Token: ✓ Disponible`.

### 5.3 POC 2: SAML 2.0
1. Accede al frontend SAML en [http://localhost:3001](http://localhost:3001).
2. Haz clic en **"Iniciar sesión con Keycloak (SAML)"**.
3. Redirigirá a Keycloak. Inicia sesión con:
   * **Usuario**: `saml-user`
   * **Contraseña**: `password`
4. Serás redirigido de vuelta al frontend SAML. Podrás consultar los datos de tu perfil y la información decodificada de la **SAML Assertion** (Subject NameID, Issuer y las condiciones temporales de validez).
5. Puedes descargar o visualizar los metadatos XML del SP generados por el backend en: [http://localhost:8001/saml/metadata](http://localhost:8001/saml/metadata).

---

---

## 6. Documentación del Flujo y Comparación

* Ver flujo detallado de OAuth/OIDC en [oauth-flow.md](file:///home/gerardo/SA-2026/Practica2/SA2026/Practica2/docs/oauth-flow.md).
* Ver flujo detallado de SAML 2.0 en [saml-flow.md](file:///home/gerardo/SA-2026/Practica2/SA2026/Practica2/docs/saml-flow.md).
* Ver análisis comparativo en [comparison.md](file:///home/gerardo/SA-2026/Practica2/SA2026/Practica2/docs/comparison.md).

---

## 7. Análisis de la POC: Funcionalidades, Beneficios, Complejidades y Escenarios

A continuación se presenta un resumen de los resultados y análisis obtenidos de la implementación de cada POC:

### 7.1 OAuth 2.0 + OpenID Connect (OIDC)

*   **Funcionalidades de la POC**:
    *   Inicio de sesión interactivo redirigiendo a Keycloak.
    *   Intercambio del código de autorización por tokens en el backend.
    *   Validación criptográfica local de tokens usando las llaves JWKS públicas de Keycloak.
    *   Cierre de sesión global (Single Logout) borrando cookies locales e invalidando la sesión en Keycloak.
    *   Consumo de un recurso protegido (`/api/profile`) utilizando cookies HttpOnly para almacenar los tokens de manera segura.
*   **Beneficios**:
    *   **Ligero y rápido**: Los tokens están en formato JSON (JWT), lo que facilita su lectura directa y reduce el tráfico de red.
    *   **Ideal para APIs**: Es sumamente fácil de implementar para autorizar endpoints en microservicios o APIs REST mediante cabeceras Bearer.
    *   **Seguridad moderna**: Soporta PKCE para mitigar la interceptación de códigos en apps móviles y frontends web.
*   **Complejidades**:
    *   Requiere implementar una lógica para el manejo de sesiones en el servidor si no se quieren exponer los tokens en la interfaz (se solucionó usando cookies de sesión HttpOnly).
    *   Configuración estricta de Redirect URIs en Keycloak para evitar redirecciones maliciosas.
*   **Escenarios de uso sugeridos**:
    *   Aplicaciones web SPA modernas (React, Vue, Angular) conectadas a APIs REST.
    *   Aplicaciones móviles nativas (Android/iOS).
    *   Sistemas basados en microservicios que requieran autorización sin estado (Stateless JWT).

### 7.2 SAML 2.0

*   **Funcionalidades de la POC**:
    *   Inicio de sesión SP-initiated generando un documento `AuthnRequest` XML firmado.
    *   Endpoint de ACS (`/saml/acs`) que recibe la respuesta SAML vía POST, valida las firmas de la Assertion usando el certificado público del IdP y extrae los claims.
    *   Cierre de sesión local y redirección al SLO de Keycloak.
    *   Generación automática de metadatos XML del SP (`/saml/metadata`) conteniendo las llaves de encriptación y endpoints.
*   **Beneficios**:
    *   **Estándar corporativo unificado**: Soporte nativo para federaciones empresariales clásicas como Active Directory Federation Services (ADFS), Okta o Ping Identity.
    *   **No requiere canal directo SP-IdP**: Como la respuesta SAML viaja a través del navegador del cliente vía POST, el servidor backend puede estar aislado de internet y seguir validando la autenticación del usuario.
    *   **Altamente configurable**: Permite definir contratos de vigencia muy estrictos (`Conditions`, `NotBefore`, `NotOnOrAfter`).
*   **Complejidades**:
    *   **Mensajes pesados**: El uso de XML y la inclusión de certificados y firmas digitales en el documento hace que la respuesta SAML sea muy grande.
    *   **Criptografía nativa compleja**: La validación de firmas XML y canonicalización requiere la instalación de librerías del sistema operativo (como `xmlsec`).
    *   **Poco amigable para móviles**: No está diseñado nativamente para aplicaciones móviles, requiriendo webviews complejos.
*   **Escenarios de uso sugeridos**:
    *   Sistemas corporativos B2B (integraciones entre empresas y proveedores de software).
    *   SSO en intranets empresariales donde las identidades se gestionan mediante Active Directory / LDAP.
    *   Aplicaciones legacy de servidor que usan cookies de sesión tradicionales en lugar de arquitecturas de API.

