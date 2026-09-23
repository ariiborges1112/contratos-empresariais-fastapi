import json
import os
from app.config import settings
from app.models.contrato import ContratoArmazenado

CAMINHO_JSON = settings.storage.diretorio_metadata + "/documentos.json"

def _ler_catalogo() -> list[ContratoArmazenado]:
    if not os.path.exists(CAMINHO_JSON):
        return []
    else:
        with open(file=CAMINHO_JSON, mode="r", encoding="utf-8") as arquivo:
            dados_dicionario = json.load(arquivo)

            contratos_validados = []

            for i in dados_dicionario:
                objeto_validado = ContratoArmazenado.model_validate(i)
                contratos_validados.append(objeto_validado)

            return contratos_validados

def _salvar_catalogo(documentos: list[ContratoArmazenado]):
    if not os.path.exists(CAMINHO_JSON):
        return []
    else:
        with open(file=CAMINHO_JSON, mode="w", enconding="utf-8") as documentos:
            dados_objetos = json.dump(ContratoArmazenado, arquivo, indent=4)

            for i in dados_objetos:
                objeto = ContratoArmazenado.model_dump()
                


    

def listar_catalogo():
    ...

def buscar_em_catalogo():
    ...

def atualizar_catalogo():
    ...

def excluir_catalogo():
    ...