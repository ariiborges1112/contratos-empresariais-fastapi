import json
import os
from app.config import settings
from app.models.contrato import ContratoArmazenado

CAMINHO_JSON = settings.storage.diretorio_metadata + "/documentos.json"

def _ler_catalogo() -> list[ContratoArmazenado]:
    if not os.path.exists(CAMINHO_JSON):
        return []
    else:
        with open(file=CAMINHO_JSON, mode="r", encoding="utf-8") as documentos:
            json.load(documentos)

            @mode

            return 
    ...

def _salvar_catalogo(documentos: list[ContratoArmazenado]):
    ...

def listar_catalogo():
    ...

def buscar_em_catalogo():
    ...

def atualizar_catalogo():
    ...

def excluir_catalogo():
    ...