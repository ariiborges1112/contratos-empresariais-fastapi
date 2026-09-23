from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent
YAML_PATH = BASE_DIR.parent / "config.yaml"

class StorageSettings(BaseModel):
    diretorio_documentos: str = "./storage/documentos"
    diretorio_backups: str = "./storage/backups"
    diretorio_logs: str = "./storage/logs"
    diretorio_metadata: str = "./storage/metadata"

class UploadSettings(BaseModel):
    max_tamanho_arquivo: int = 10485760  # 10 MB em bytes
    formatos_permitidos: list[str] = [".pdf", ".docx", ".txt", ".jpg", ".png"]

class HashSettings(BaseModel):
    algoritmo: str = "sha256"

class LoggingSettings(BaseModel):
    nivel: str = "INFO"
    arquivo: str = "./storage/logs/sistema.log"

class BackupSettings(BaseModel):
    frequencia: str = "diaria"
    formato: str = "zip"

class ContratoSettings(BaseModel):
    dias_alerta_vencimento: int = 30

class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        if not YAML_PATH.exists():
            return {}
        with open(YAML_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

class Settings(BaseSettings):
    storage: StorageSettings = Field(default_factory=StorageSettings)
    upload: UploadSettings = Field(default_factory=UploadSettings)
    hash: HashSettings = Field(default_factory=HashSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    backup: BackupSettings = Field(default_factory=BackupSettings)
    contrato: ContratoSettings = Field(default_factory=ContratoSettings)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
       
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
        )

settings = Settings()