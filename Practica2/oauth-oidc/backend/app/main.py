from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.config import settings

app = FastAPI(
    title="OAuth 2.0 + OIDC Proof of Concept",
    description="Backend de la POC de OIDC con FastAPI",
    version="1.0.0"
)

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.OAUTH_FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar las rutas
app.include_router(router)

@app.get("/")
def index():
    return {
        "message": "Backend de OIDC funcionando",
        "docs": "/docs",
        "endpoints": {
            "login": "/login",
            "logout": "/logout",
            "profile": "/api/profile",
            "health": "/health"
        }
    }
