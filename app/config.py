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

