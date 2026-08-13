import os

class Settings:
    KEYCLOAK_URL: str = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
    KEYCLOAK_URL_INTERNAL: str = os.getenv("KEYCLOAK_URL_INTERNAL", "http://keycloak:8080")
    SAML_REALM: str = os.getenv("SAML_REALM", "saml-realm")
    SAML_FRONTEND_URL: str = os.getenv("SAML_FRONTEND_URL", "http://localhost:3001")
    SAML_BACKEND_URL: str = os.getenv("SAML_BACKEND_URL", "http://localhost:8001")
    
    # Parametros SAML
    SAML_ENTITY_ID: str = os.getenv("SAML_ENTITY_ID", "http://localhost:8001/saml/metadata")
    SAML_ACS_URL: str = os.getenv("SAML_ACS_URL", "http://localhost:8001/saml/acs")
    
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "saml-session-secret-key-999")
    CERT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "certs"))

    @property
    def idp_sso_url(self) -> str:
        # Enpoint SSO de Keycloak
        return f"{self.KEYCLOAK_URL}/realms/{self.SAML_REALM}/protocol/saml"

    @property
    def idp_sso_url_internal(self) -> str:
        return f"{self.KEYCLOAK_URL_INTERNAL}/realms/{self.SAML_REALM}/protocol/saml"

    @property
    def idp_entity_id(self) -> str:
        return f"{self.KEYCLOAK_URL}/realms/{self.SAML_REALM}"

    @property
    def idp_slo_url(self) -> str:
        # Endpoint SLO de Keycloak para desloguear
        return f"{self.KEYCLOAK_URL}/realms/{self.SAML_REALM}/protocol/saml"

settings = Settings()
