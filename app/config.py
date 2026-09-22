from pathlib import Path
from typing import Any, Dict, Type
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict
)

BASE_DIR = Path(__file__).resolve().parent
YAML_PATH = BASE_DIR / "config.yaml"

class StorageSenttings(BaseModel):
    diretorio_documentos:str = "./storage/documentos"
    diretorio_metadata: str = "./storage/metadata"
    diretorio_backups: str = "./storage/backups"
    diretorio_exportados: str = "./storage/exportados"


class UploadSenttings(BaseModel):
    tamanho_max: int = 20


class HashSenttings(BaseModel):
    algoritmo: str = "sha256"

class LoggingSentings(BaseModel):
    arquivo: str = "./storage/logs/sistema.log"
    nivel: str = "INFO"

class BackupSenttings(BaseModel):
    formato: str = "zip"


class Senttings(BaseSettings):
    storage: StorageSenttings = Field(default_factory=StorageSenttings)
    upload: UploadSenttings = Field(default_factory=UploadSenttings)
    hash: HashSenttings = Field(default_factory=HashSenttings)
    logging: LoggingSentings = Field(default_factory=LoggingSentings)
    backup: BackupSenttings = Field(default_factory=BackupSenttings)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra= "ignore",
    )


    

