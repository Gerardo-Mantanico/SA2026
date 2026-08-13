from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.config import settings

app = FastAPI(
    title="SAML 2.0 Proof of Concept",
    description="Backend de la POC de SAML con FastAPI",
    version="1.0.0"
)

# Configurar CORS para la interfaz
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.SAML_FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar las rutas
app.include_router(router)

@app.get("/")
def index():
    return {
        "message": "Backend de SAML funcionando",
        "docs": "/docs",
        "endpoints": {
            "login": "/login",
            "logout": "/logout",
            "metadata": "/saml/metadata",
            "profile": "/api/profile",
            "health": "/health"
        }
    }
