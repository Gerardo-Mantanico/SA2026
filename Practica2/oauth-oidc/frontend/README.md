# OAuth 2.0 + OIDC Frontend

Esta es la aplicación web de interfaz (Frontend) de la **Proof of Concept (POC) de OAuth 2.0 y OpenID Connect (OIDC)**. Está construida con React, Vite y Tailwind CSS, y se comunica con el backend de FastAPI en el puerto `8000`.

## 1. Objetivo
Proporcionar una interfaz limpia y estética para que el usuario pueda:
* Iniciar el flujo de autenticación (Login).
* Ver el estado de autenticación de su sesión en tiempo real.
* Consultar la información del usuario autenticado (Name, Email, Username) proveniente de los Claims del ID Token.
* Visualizar la disponibilidad del Access Token.
* Finalizar la sesión (Logout).

## 2. Tecnologías
* **React 18**
* **Vite** (Herramienta de compilación rápida)
* **Tailwind CSS** (Framework de diseño con estilos premium)

## 3. Funcionamiento
El frontend no almacena secretos del cliente ni tokens en el almacenamiento local del navegador (como `localStorage` o `sessionStorage`). Toda la autenticación se gestiona de forma segura mediante cookies HttpOnly a través del FastAPI backend, protegiendo al usuario contra ataques de robo de tokens (XSS).

La comunicación con el backend utiliza el parámetro `credentials: 'include'` en las peticiones `fetch` para enviar las cookies automáticas del navegador.

## 4. Ejecución local (sin Docker)
1. Instalar dependencias:
   ```bash
   npm install
   ```
2. Ejecutar el servidor de desarrollo:
   ```bash
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:3000`.
