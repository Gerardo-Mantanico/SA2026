import requests
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from app.config import settings
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyCookie

# Cookie para guardar la sesion
cookie_sec = APIKeyCookie(name="session_token", auto_error=False)

# Cache para las llaves de Keycloak
_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        try:
            response = requests.get(settings.jwks_url, timeout=5)
            response.raise_for_status()
            _jwks_cache = response.json()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener JWKS de Keycloak: {str(e)}"
            )
    return _jwks_cache

def verify_token(token: str) -> dict:
    """ Valida el token JWT usando las llaves de Keycloak """
    jwks = get_jwks()
    try:
        # Sacar el kid del header del token
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise JWTError("Falta el kid en el header")
        
        # Buscar la llave correspondiente
        key = None
        for k in jwks.get("keys", []):
            if k.get("kid") == kid:
                key = k
                break
        
        if not key:
            # Reintentar limpiando la cache
            global _jwks_cache
            _jwks_cache = None
            jwks = get_jwks()
            for k in jwks.get("keys", []):
                if k.get("kid") == kid:
                    key = k
                    break
            if not key:
                raise JWTError("No se encontro la llave en JWKS")
        
        # Validar firma, emisor y audiencia
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.OAUTH_CLIENT_ID,
            issuer=settings.keycloak_issuer
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesion ha expirado"
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalido: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de autenticacion: {str(e)}"
        )

def get_current_user(session_token: str = Security(cookie_sec)):
    """ Retorna el usuario si el token de sesion es valido """
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hay sesion activa"
        )
    
    # Decodificar el token y extraer claims del usuario
    claims = verify_token(session_token)
    return {
        "name": claims.get("name", claims.get("preferred_username")),
        "email": claims.get("email"),
        "username": claims.get("preferred_username"),
        "sub": claims.get("sub")
    }
