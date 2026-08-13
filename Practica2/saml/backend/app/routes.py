import json
from fastapi import APIRouter, Response, Request, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie
from itsdangerous import Signer, BadSignature

from app.config import settings
from app.auth import prepare_fastapi_request, init_saml_auth, get_saml_settings
from onelogin.saml2.settings import OneLogin_Saml2_Settings

router = APIRouter()
cookie_sec = APIKeyCookie(name="saml_session", auto_error=False)
signer = Signer(settings.SESSION_SECRET_KEY)

@router.get("/health")
def health():
    return {"status": "ok", "service": "saml-backend"}

@router.get("/login")
async def login(request: Request):
    """ Redirige al login de Keycloak con el SAMLRequest """
    req = await prepare_fastapi_request(request)
    auth = init_saml_auth(req)
    # Generar la URL de redireccion del IdP
    redirect_url = auth.login()
    return RedirectResponse(url=redirect_url)

@router.post("/saml/acs")
async def acs(request: Request):
    """ Recibe la respuesta SAML en el formulario POST de Keycloak """
    req = await prepare_fastapi_request(request)
    auth = init_saml_auth(req)
    
    # Procesar respuesta SAML
    auth.process_response()
    
    # Comprobar si hubo errores en la validacion del XML
    errors = auth.get_errors()
    if errors:
        error_reason = auth.get_last_error_reason()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Fallo la validacion SAML: {errors}. Detalle: {error_reason}"
        )
        
    if not auth.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo autenticar al usuario"
        )
        
    # Obtener atributos del usuario mapeados desde la assertion
    attributes = auth.get_attributes()
    name_id = auth.get_nameid()
    
    email_list = attributes.get("email", [])
    username_list = attributes.get("username", [])
    firstname_list = attributes.get("firstName", [])
    lastname_list = attributes.get("lastName", [])
    
    email = email_list[0] if email_list else ""
    username = username_list[0] if username_list else name_id
    first_name = firstname_list[0] if firstname_list else "SAML"
    last_name = lastname_list[0] if lastname_list else "User"
    
    # Extraer NotBefore del XML ya que python3-saml no tiene metodo directo para este claim
    xml_str = auth.get_last_response_xml()
    import re
    not_before = None
    if xml_str:
        match = re.search(r'NotBefore="([^"]+)"', xml_str)
        if match:
            not_before = match.group(1)

    user_data = {
        "username": username,
        "email": email,
        "name": f"{first_name} {last_name}".strip(),
        "name_id": name_id,
        "issuer": auth.get_settings().get_idp_data().get('entityId'),
        "session_index": auth.get_session_index(),
        "conditions": {
            "not_before": not_before,
            "not_on_or_after": auth.get_last_assertion_not_on_or_after()
        }
    }
    
    # Guardar los datos en una cookie de sesion firmada
    signed_session = signer.sign(json.dumps(user_data).encode()).decode()
    
    # Redirigir de vuelta a la interfaz frontend de SAML
    response = RedirectResponse(url=settings.SAML_FRONTEND_URL, status_code=status.HTTP_303_SEE_OTHER)
    
    # Escribir la cookie en el navegador
    response.set_cookie(
        key="saml_session",
        value=signed_session,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    
    return response

@router.get("/saml/metadata")
def metadata():
    """ Genera el XML de metadatos del SP """
    try:
        saml_settings = get_saml_settings()
        sp_settings = OneLogin_Saml2_Settings(saml_settings)
        metadata_xml = sp_settings.get_sp_metadata()
        errors = sp_settings.validate_metadata(metadata_xml)
        
        if errors:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Metadatos del SP invalidos: {errors}"
            )
            
        return Response(content=metadata_xml, media_type="application/xml")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo generar metadatos: {str(e)}"
        )

@router.get("/api/profile")
def get_profile(saml_session: str = Depends(cookie_sec)):
    """ Endpoint protegido que lee la cookie firmada """
    if not saml_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hay sesion SAML activa"
        )
        
    try:
        # Validar la firma de la cookie
        unsigned_data = signer.unsign(saml_session.encode()).decode()
        user_data = json.loads(unsigned_data)
        return {
            "authenticated": True,
            "user": {
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "username": user_data.get("username")
            },
            "assertion": {
                "subject_name_id": user_data.get("name_id"),
                "issuer": user_data.get("issuer"),
                "session_index": user_data.get("session_index"),
                "not_before": user_data.get("conditions", {}).get("not_before"),
                "not_on_or_after": user_data.get("conditions", {}).get("not_on_or_after")
            }
        }
    except BadSignature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma de sesion invalida"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al decodificar sesion: {str(e)}"
        )

@router.get("/logout")
def logout():
    """ Limpia la cookie local y redirige al logout de Keycloak """
    response = RedirectResponse(url=settings.SAML_FRONTEND_URL)
    response.delete_cookie("saml_session", path="/")
    
    # URL de Keycloak para desloguear la sesion SAML con redirect_uri para retornar
    keycloak_logout_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.SAML_REALM}/protocol/saml/logout"
        f"?redirect_uri={settings.SAML_FRONTEND_URL}"
    )
    response.headers["Location"] = keycloak_logout_url
    
    return response
