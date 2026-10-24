"""Configuration management."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="127.0.0.1", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")

    llm_provider: str = Field(default="custom", alias="LLM_PROVIDER")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_model: str = Field(default="gemma4-e4b", alias="LLM_MODEL")
    llm_base_url: str = Field(default="http://localhost:8080/v1", alias="LLM_BASE_URL")

    keycloak_url: str = Field(default="http://localhost:8081", alias="KEYCLOAK_URL")
    keycloak_realm: str = Field(default="axiom-lens", alias="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(default="axiom-lens-client", alias="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(default="", alias="KEYCLOAK_CLIENT_SECRET")

    database_url: str = Field(default="sqlite:///./axiom_lens.db", alias="DATABASE_URL")

    adb_host: str = Field(default="127.0.0.1", alias="ADB_HOST")
    adb_port: int = Field(default=5037, alias="ADB_PORT")
    allow_remote_adb: bool = Field(default=False, alias="ARTEMIS_ALLOW_REMOTE_ADB_CONFIGURATION")

    @property
    def cors_origins(self) -> list[str]:
        if self.app_env == "development":
            return ["http://localhost:5173", "http://127.0.0.1:5173"]
        return []


settings = Settings()
