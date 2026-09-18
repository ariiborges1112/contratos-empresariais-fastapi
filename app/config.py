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

class StorageSentings(BaseModel):
    diretorio_documentos:str = "./storage/documentos"
    diretorio_metadata: str = "./storage/metadata"
    diretorio_backups: str = "./storage/backups"
    diretorio_exportados: str = "./storage/exportados"