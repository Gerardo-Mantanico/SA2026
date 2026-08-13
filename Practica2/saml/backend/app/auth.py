import os
import requests
import xml.etree.ElementTree as ET
from fastapi import Request, HTTPException, status
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from app.config import settings

_cached_cert = None

def get_idp_signing_cert() -> str:
    """ Baja el XML de metadatos de Keycloak y extrae el certificado publico """
    global _cached_cert
    if _cached_cert is not None:
        return _cached_cert

    url = f"{settings.KEYCLOAK_URL_INTERNAL}/realms/{settings.SAML_REALM}/protocol/saml/descriptor"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        xml_content = response.content
    except Exception as e:
        # Keycloak no responde o no ha iniciado
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Keycloak no disponible: {str(e)}"
        )

    try:
        # Parsear el XML para buscar el certificado de Keycloak
        root = ET.fromstring(xml_content)
        ns = {
            'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
        
        # Buscar el certificado de firma
        cert_node = root.find(".//md:IDPSSODescriptor/md:KeyDescriptor[@use='signing']//ds:X509Certificate", ns)
        if cert_node is None:
            # Buscar el primer certificado que encuentre
            cert_node = root.find(".//ds:X509Certificate", ns)
            
        if cert_node is not None and cert_node.text:
            _cached_cert = cert_node.text.strip().replace("\n", "").replace(" ", "")
            return _cached_cert
            
        raise ValueError("No se encontro la etiqueta X509Certificate")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el certificado SAML de Keycloak: {str(e)}"
        )

def get_saml_settings() -> dict:
    """ Carga las configuraciones del SP y el IdP para python3-saml """
    sp_key_path = os.path.join(settings.CERT_DIR, "sp.key")
    sp_cert_path = os.path.join(settings.CERT_DIR, "sp.crt")
    
    if not os.path.exists(sp_key_path) or not os.path.exists(sp_cert_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Faltan las llaves del SP en la carpeta certs"
        )
        
    with open(sp_key_path, "r") as f:
        sp_key = f.read()
    with open(sp_cert_path, "r") as f:
        sp_cert = f.read()
        
    idp_cert = get_idp_signing_cert()
    
    return {
        "strict": True,
        "debug": True,
        "sp": {
            "entityId": settings.SAML_ENTITY_ID,
            "assertionConsumerService": {
                "url": settings.SAML_ACS_URL,
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "singleLogoutService": {
                "url": f"{settings.SAML_BACKEND_URL}/saml/logout",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": sp_cert,
            "privateKey": sp_key
        },
        "idp": {
            "entityId": settings.idp_entity_id,
            "singleSignOnService": {
                "url": settings.idp_sso_url,
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "singleLogoutService": {
                "url": settings.idp_slo_url,
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": idp_cert
        },
        "security": {
            "nameIdEncrypted": False,
            "authnRequestsSigned": False,
            "logoutRequestSigned": False,
            "logoutResponseSigned": False,
            "signMetadata": False,
            "wantMessagesSigned": True,
            "wantAssertionsSigned": True,
            "wantAssertionsEncrypted": False,
            "wantNameId": True,
            "wantNameIdEncrypted": False,
            "signatureAlgorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
            "digestAlgorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
        }
    }

async def prepare_fastapi_request(request: Request) -> dict:
    """ Convierte la peticion de FastAPI al formato que usa python3-saml """
    form_data = {}
    if request.method == "POST":
        # Leer formulario si es POST (para la respuesta de Keycloak)
        form = await request.form()
        form_data = {k: v for k, v in form.items()}
        
    proto = request.headers.get("x-forwarded-proto", "http")
    is_https = "on" if proto == "https" or request.url.scheme == "https" else "off"
    
    return {
        "https": is_https,
        "http_host": request.headers.get("host", "localhost:8001"),
        "script_name": request.url.path,
        "get_data": dict(request.query_params),
        "post_data": form_data
    }

def init_saml_auth(req: dict) -> OneLogin_Saml2_Auth:
    """ Inicializa la libreria de SAML con la peticion """
    saml_settings = get_saml_settings()
    return OneLogin_Saml2_Auth(req, saml_settings)
