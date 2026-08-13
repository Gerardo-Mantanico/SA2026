import requests
from fastapi import APIRouter, Response, Request, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie
from app.config import settings
from app.auth import get_current_user, cookie_sec, verify_token

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "oauth-oidc-backend"}

@router.get("/login")
def login():
    """ Redirige al login de Keycloak """
    # URL de redireccion de vuelta al backend
    redirect_uri = f"{settings.OAUTH_BACKEND_URL}/callback"
    auth_url = (
        f"{settings.auth_url}"
        f"?client_id={settings.OAUTH_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid+profile+email"
        f"&redirect_uri={redirect_uri}"
    )
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def callback(code: str = None, error: str = None, error_description: str = None):
    """ Procesa el codigo que manda Keycloak y pide los tokens """
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de Keycloak: {error} - {error_description}"
        )
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Falta el codigo de autorizacion"
        )

    # Parametros para intercambiar el codigo por token
    redirect_uri = f"{settings.OAUTH_BACKEND_URL}/callback"
    payload = {
        "grant_type": "authorization_code",
        "client_id": settings.OAUTH_CLIENT_ID,
        "client_secret": settings.OAUTH_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(settings.token_url, data=payload, headers=headers, timeout=5)
        response.raise_for_status()
        tokens = response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo el intercambio de tokens: {str(e)}"
        )

    access_token = tokens.get("access_token")
    id_token = tokens.get("id_token")

    if not id_token or not access_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Faltan tokens en la respuesta"
        )

    # Validar el token de identidad
    verify_token(id_token)

    # Redirigir de vuelta al frontend
    response = RedirectResponse(url=settings.OAUTH_FRONTEND_URL)
    
    # Guardar tokens en cookies HttpOnly por seguridad
    response.set_cookie(
        key="session_token",
        value=id_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    
    return response

@router.get("/api/profile")
def get_profile(
    current_user: dict = Depends(get_current_user),
    access_token: str = Depends(APIKeyCookie(name="access_token", auto_error=False))
):
    """ Retorna los datos del perfil si esta autenticado """
    access_token_available = access_token is not None
    return {
        "authenticated": True,
        "user": current_user,
        "access_token_available": access_token_available
    }

@router.get("/logout")
def logout(
    request: Request,
    session_token: str = Depends(cookie_sec)
):
    """ Borra la sesion y desloguea en Keycloak """
    response = RedirectResponse(url=settings.OAUTH_FRONTEND_URL)
    response.delete_cookie("session_token", path="/")
    response.delete_cookie("access_token", path="/")
    
    if session_token:
        # Redirigir a Keycloak para cerrar sesion global
        logout_redirect = (
            f"{settings.logout_url}"
            f"?id_token_hint={session_token}"
            f"&post_logout_redirect_uri={settings.OAUTH_FRONTEND_URL}"
        )
        response.headers["Location"] = logout_redirect

    return response
