import os

class Settings:
    KEYCLOAK_URL: str = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
    KEYCLOAK_URL_INTERNAL: str = os.getenv("KEYCLOAK_URL_INTERNAL", "http://keycloak:8080")
    OAUTH_REALM: str = os.getenv("OAUTH_REALM", "oauth-realm")
    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID", "oauth-client")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET", "oauth-client-secret-12345")
    OAUTH_FRONTEND_URL: str = os.getenv("OAUTH_FRONTEND_URL", "http://localhost:3000")
    OAUTH_BACKEND_URL: str = os.getenv("OAUTH_BACKEND_URL", "http://localhost:8000")
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "oauth-session-secret-key-999")

    @property
    def keycloak_issuer(self) -> str:
        # El emisor del token (visto por el navegador externo)
        return f"{self.KEYCLOAK_URL}/realms/{self.OAUTH_REALM}"

    @property
    def jwks_url(self) -> str:
        return f"{self.KEYCLOAK_URL_INTERNAL}/realms/{self.OAUTH_REALM}/protocol/openid-connect/certs"

    @property
    def token_url(self) -> str:
        return f"{self.KEYCLOAK_URL_INTERNAL}/realms/{self.OAUTH_REALM}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return f"{self.KEYCLOAK_URL}/realms/{self.OAUTH_REALM}/protocol/openid-connect/auth"

    @property
    def logout_url(self) -> str:
        return f"{self.KEYCLOAK_URL}/realms/{self.OAUTH_REALM}/protocol/openid-connect/logout"

settings = Settings()
