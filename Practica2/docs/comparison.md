# Comparativa de Protocolos: OAuth 2.0 / OIDC vs SAML 2.0

Este documento presenta una comparación exhaustiva entre **OAuth 2.0 + OpenID Connect (OIDC)** y **SAML 2.0**, basada en las implementaciones de Proof of Concept (POC) desarrolladas en este proyecto.

---

## 1. Tabla Comparativa General

| Característica | OAuth 2.0 + OIDC | SAML 2.0 |
| :--- | :--- | :--- |
| **Tipo** | Framework de autorización + Capa de identidad | Estándar de federación de identidades (SSO) |
| **Formato de Mensajes** | JSON / JWT (JSON Web Tokens) | XML / SAML Assertion |
| **Flujo Predominante** | Basado en REST / API / Redirección | Redirección de navegador + HTTP POST |
| **Mecanismo de Intercambio** | Peticiones HTTP directas (Server-side) y API | Intercambio indirecto vía navegador del cliente |
| **Tokens / Credenciales** | Access Token, ID Token, Refresh Token | SAML Assertion |
| **Criptografía** | Firmas JWS / Encriptación JWE (JWT) | Firmas XMLDSig / Cifrado XML |
| **Consumo de APIs** | Altamente optimizado (Bearer Token) | Complejo, no diseñado nativamente para APIs |
| **Uso Frecuente** | Apps web SPA, móviles, microservicios, IoT | Intranets corporativas, portales B2B, Legacy |
| **Complejidad de Setup** | Baja-Media (JSON, endpoints REST estándar) | Alta (Certificados x509, namespaces XML, metadatos) |
| **Cierre de Sesión (SLO)** | OIDC Session/Front/Backchannel logout | Single Logout Service (SLO XML redirects) |

---

## 2. Análisis Detallado por Tecnología

### 2.1 OAuth 2.0 + OpenID Connect (OIDC)

OIDC es una capa de identidad construida sobre OAuth 2.0 (un framework de autorización). Proporciona a las aplicaciones información estructurada sobre el usuario autenticado a través del **ID Token** y la capacidad de actuar en nombre del usuario mediante el **Access Token**.

#### Beneficios
* **Integración Moderna**: Al estar basado en JSON, es extremadamente fácil de parsear en JavaScript, Python, móviles y cualquier lenguaje moderno.
* **Granularidad en APIs**: Permite proteger microservicios de forma sencilla transmitiendo el Access Token en la cabecera `Authorization: Bearer <token>`.
* **Soporte Móvil y de Clientes SPA**: Flujos como Authorization Code con PKCE están específicamente optimizados para mitigar riesgos en plataformas donde no se pueden guardar secretos.
* **Separación de Responsabilidades**: Distingue claramente entre autenticación (quién eres - OIDC) y autorización (qué puedes hacer - OAuth 2.0).

#### Complejidades
* **Manejo de Ciclo de Vida**: El refresco de tokens (`Refresh Tokens`) requiere un almacenamiento seguro y lógica de renovación constante en el cliente.
* **Múltiples Tokens**: Requiere gestionar y validar tokens separados (ID Token vs Access Token), lo cual puede confundir a desarrolladores novatos.

---

### 2.2 SAML 2.0 (Security Assertion Markup Language)

SAML 2.0 es un estándar basado en XML que permite la federación de identidades. Permite que un Identity Provider (Keycloak) comparta credenciales de autenticación y atributos con un Service Provider (FastAPI) de forma segura.

#### Beneficios
* **SSO Corporativo Consolidado**: Es el estándar de oro en redes corporativas (Active Directory, Okta, Ping Identity). Permite SSO entre múltiples aplicaciones empresariales sin compartir base de datos.
* **Madurez y Robustez**: Lleva más de 15 años en el mercado. Sus reglas de confianza mediante el intercambio de metadatos XML son muy estrictas.
* **No Requiere Canales Directos SP-IdP**: Toda la comunicación fluye a través del navegador del cliente (HTTP Redirect y HTTP POST). Esto permite que el backend esté en una red interna privada sin acceso a Internet, siempre que el usuario pueda ver al IdP.

#### Complejidades
* **Sobrecarga de Datos (XML)**: Los mensajes SAML son extremadamente pesados debido al formato XML y la inclusión de certificados completos y firmas en línea.
* **Complejidad Criptográfica**: Configurar correctamente la validación de firmas digitales, canonicalización de XML (C14N) y descifrado de assertions requiere librerías nativas complejas (como `xmlsec`).
* **Soporte Móvil Deficiente**: Al depender de redirecciones de navegador completas y envíos de formularios POST automáticos, es difícil de integrar en aplicaciones nativas móviles.

---

## 3. Escenarios de Implementación Recomendados

### Cuándo elegir OAuth 2.0 + OIDC:
1. **Desarrollo de APIs y Microservicios**: Si la aplicación expone endpoints REST/gRPC que serán consumidos por frontends móviles o SPA.
2. **Aplicaciones Móviles Nativas**: OIDC es nativo y soporta flujos con PKCE.
3. **Plataformas Modernas basadas en la Nube**: Arquitecturas serverless y distribuidas que se benefician de JWT autovalidados sin estado.

### Cuándo elegir SAML 2.0:
1. **Entorno Corporativo / B2B**: Integración con clientes empresariales que exigen federación mediante Active Directory Federation Services (ADFS), Shibboleth u Okta.
2. **Aplicaciones Web Legacy**: Sistemas empresariales clásicos que no manejan arquitecturas de APIs tipo REST, sino sesiones de servidor tradicionales basadas en cookies.
3. **Restricciones de Red Estrictas**: Cuando el servidor de la aplicación (SP) no puede realizar peticiones directas de red hacia el servidor de identidad (IdP), requiriendo que toda la autenticación ocurra a través del cliente.
