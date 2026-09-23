import json
import os
from app.config import settings
from app.models.contrato import ContratoArmazenado, ContratoUpdate

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

#F1
def _salvar_catalogo(documentos: list[ContratoArmazenado]):
    with open(file=CAMINHO_JSON, mode="w", encoding="utf-8") as arquivo:
        dados_para_salvar = []

        for i in documentos:
            dicionario = i.model_dump()
            dados_para_salvar.append(dicionario)

        json.dump(dados_para_salvar, arquivo, indent=4)

#F1
def 

#F2, F7                
def listar_documentos(contratante: str | None = None, situacao: str | None = None,
                      categoria: str | None = None, extensao: str | None = None) -> list[ContratoArmazenado]:
    contratos = _ler_catalogo()

    if contratante:
        contratos = [i for i in contratos if i.contratante == contratante]

    if situacao:
        contratos = [i for i in contratos if i.situacao == situacao]

    if categoria:
        contratos = [i for i in contratos if i.categoria == categoria]

    if extensao:
        contratos = [i for i in contratos if i.extensao == extensao]

    return contratos

#F3
def buscar_documento_via_id(id: int) -> ContratoArmazenado | None:
    contratos = _ler_catalogo()

    for i in contratos:
        if i.id == id:
            return i

    return None

#F5
def atualizar_documento(id: int, dados_atualizados: ContratoUpdate) -> ContratoArmazenado | None:
    contratos = _ler_catalogo()

    for contrato in contratos:
        if contrato.id == id:
            novos_dados = dados_atualizados.model_dump(exclude_unset=True)

            for chave, valor in novos_dados.items():
                setattr(contrato, chave, valor)

            _salvar_catalogo(contratos)

            return contrato

    return None

#F6
def excluir_documento(id: int):
    contratos = _ler_catalogo()
    contrato_alvo = buscar_documento_via_id(id)

    if contrato_alvo:
        contratos.remove(contrato_alvo)

        _salvar_catalogo(contratos)

        caminho_arquivo = os.path.join(settings.storage.diretorio_documentos, contrato_alvo.nome_armazenado)
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

        return True

    return False