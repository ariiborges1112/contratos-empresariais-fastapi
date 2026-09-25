import json
import os
import logging
import mimetypes
from app.services.hash_service import calcular_hash_bytes
from datetime import date, timedelta, datetime
from app.config import settings
from app.models.contrato import ContratoCreate, ContratoArmazenado, ContratoUpdate, SituacaoContrato

logger = logging.getLogger()

CAMINHO_JSON = settings.storage.diretorio_metadata + "/documentos.json"

os.makedirs(settings.storage.diretorio_metadata, exist_ok=True)
os.makedirs(settings.storage.diretorio_documentos, exist_ok=True)

def _ler_catalogo() -> list[ContratoArmazenado]:
    if not os.path.exists(CAMINHO_JSON):
        return []
    else:
        with open(file=CAMINHO_JSON, mode="r", encoding="utf-8") as arquivo:
            dados_dicionario = json.load(arquivo)

            contratos_validados = []

            for i in dados_dicionario:
                objeto_validado = ContratoArmazenado.model_validate(i)

                objeto_validado.situacao = _calcular_situacao(objeto_validado.data_termino)

                contratos_validados.append(objeto_validado)

            return contratos_validados

def _salvar_catalogo(documentos: list[ContratoArmazenado]):
    with open(file=CAMINHO_JSON, mode="w", encoding="utf-8") as arquivo:
        dados_para_salvar = []

        for i in documentos:
            dicionario = i.model_dump(mode="json")
            dados_para_salvar.append(dicionario)

        json.dump(dados_para_salvar, arquivo, indent=4)

def _calcular_situacao(data_termino: date) -> SituacaoContrato:
    hoje = date.today()
    dias_alerta = settings.contrato.dias_alerta_vencimento

    if data_termino < hoje:
        return SituacaoContrato.VENCIDO
    elif hoje <= data_termino <= hoje + timedelta(days=dias_alerta):
        return SituacaoContrato.PRE_VENCIDO
    else: 
        return SituacaoContrato.VIGENTE
    
#F1
def salvar_documentos(dados: ContratoCreate, nome_arquivo_original: str, conteudo_arquivo: bytes) -> ContratoArmazenado:
    contratos = _ler_catalogo()

    
    novo_id = max([i.id for i in contratos], default=0) + 1

     
    _, extensao = os.path.splitext(nome_arquivo_original)
    nome_armazenado = f"{novo_id}_{nome_arquivo_original}"

    
    os.makedirs(settings.storage.diretorio_documentos, exist_ok=True)
    caminho_completo = os.path.join(settings.storage.diretorio_documentos, nome_armazenado)

    _, extensao = os.path.splitext(nome_arquivo_original)
    nome_armazenado = f"{novo_id}_{nome_arquivo_original}"
    caminho_completo = os.path.join(settings.storage.diretorio_documentos, nome_armazenado)

   
    sha256_hash = calcular_hash_bytes(conteudo_arquivo)
    tipo_mime, _ = mimetypes.guess_type(nome_arquivo_original)
    tipo_mime = tipo_mime or "application/octet-stream"
    tamanho_arquivo = len(conteudo_arquivo)

    
    situacao_calculada = _calcular_situacao(dados.data_termino)

    
    novo_contrato = ContratoArmazenado(
        id=novo_id,
        nome_original=nome_arquivo_original,
        nome_armazenado=nome_armazenado,
        extensao=extensao,
        tipo_mime=tipo_mime,
        tamanho=tamanho_arquivo,
        situacao=situacao_calculada,
        data_upload=datetime.now(),
        sha256=sha256_hash,
        **dados.model_dump()  
    )

    
    contratos.append(novo_contrato)
    _salvar_catalogo(contratos)

    return novo_contrato



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

#F4
def download_documentos(id: int) -> tuple[str, str, str] | None:
    contrato = buscar_documento_via_id(id)
    if not contrato:
        return None

    caminho_arquivo = os.path.join(
        settings.storage.diretorio_documentos,
        contrato.nome_armazenado
    )

    if not os.path.exists(caminho_arquivo):
        return None


    return caminho_arquivo, contrato.nome_original, contrato.tipo_mime
    

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

    #lista filtrada, """removendo""" o documento do id passado como parametro
    contratos_filtrados = [c for c in contratos if c.id != id]

    if len(contratos_filtrados) == len(contratos):
        return False

    contrato_alvo = next(c for c in contratos if c.id == id)

    _salvar_catalogo(contratos_filtrados)

    caminho_arquivo = os.path.join(
        settings.storage.diretorio_documentos, 
        contrato_alvo.nome_armazenado
    )

    try:
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
    except OSError as e:
        logger.error(f"Não foi possivel remover o arquivo {caminho_arquivo}: {e}")

    return True