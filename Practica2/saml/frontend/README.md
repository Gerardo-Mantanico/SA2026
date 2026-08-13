# SAML 2.0 Frontend

Esta es la aplicación de interfaz (Frontend) de la **Proof of Concept (POC) de SAML 2.0**. Está construida con React, Vite y Tailwind CSS, y se conecta con el Service Provider (FastAPI) en el puerto `8001`.

## 1. Objetivo
Proporcionar una interfaz moderna y descriptiva que demuestre el flujo de federación de identidad. Permite al usuario:
* Iniciar el flujo de inicio de sesión único (SAML SSO).
* Visualizar el estado de sesión actual.
* Consultar la información del usuario autenticado mapeada de la Assertion SAML.
* Examinar los metadatos de la Assertion SAML: el identificador del sujeto (`Subject NameID`), el emisor (`Issuer`), el índice de sesión y el período de validez temporal (`Conditions` de vigencia: `NotBefore` y `NotOnOrAfter`).
* Cerrar sesión de forma segura a través de SLO.

## 2. Tecnologías
* **React 18**
* **Vite** (Build tooling)
* **Tailwind CSS** (Framework de diseño)

## 3. Funcionamiento
La interfaz se conecta con el Service Provider de FastAPI. Al igual que la POC de OIDC, no guarda credenciales sensibles en el almacenamiento local del cliente. El backend firma y gestiona cookies seguras HttpOnly (`saml_session`), las cuales el frontend incluye de forma transparente en sus llamadas mediante `credentials: 'include'`.

Adicionalmente, se incluye un enlace rápido hacia el endpoint público de metadatos XML `/saml/metadata` del backend.

## 4. Ejecución local (sin Docker)
1. Instalar dependencias:
   ```bash
   npm install
   ```
2. Iniciar el servidor:
   ```bash
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:3001`.
